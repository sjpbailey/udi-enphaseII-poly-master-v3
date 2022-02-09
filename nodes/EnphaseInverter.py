"""
Polyglot v3 node server Enphase
Copyright (C) 2021 Steven Bailey

MIT License
"""
from random import randint
from time import sleep
import udi_interface
from datetime import datetime, timedelta
import time
import json
import urllib3
#import logging
import pandas as pd
import numpy as np
from numpy import random
import requests
from requests.auth import HTTPBasicAuth  # HTTP

from nodes import EnphaseController
from nodes import EnphaseNode

LOGGER = udi_interface.LOGGER


class InverterNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, system_id, key, user_id, inv_idx):
        super(InverterNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.system_id = system_id
        self.key = key
        self.user_id = user_id
        self.inv_idx = int(inv_idx)

    def start(self):
        self.http = urllib3.PoolManager()
        time.sleep(15)
        sleeptime = random.uniform(60, 240)
        sleep(sleeptime)
        LOGGER.info("sleeping is over")
        self.getpower(self)

    def getpower(self, command):
        self.inv_idx = int(self.inv_idx)
        inv_site = int(0)
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
            self.system_id
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r2 = requests.get(URL_SITE, params=params)
            # LOGGER.info(r2)
            Response2 = json.loads(r2.text)
            if r2.status_code == 200:
                self.setDriver('ST', 1)
            else:
                self.setDriver('ST', 0)
            if r2.status_code == 409:
                LOGGER.infor('You have EXCEEDED Your Monthly Hit Rate')
            else:
                pass
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
        #### Sort Inverter Data ####
        df = pd.json_normalize(
            Response2[int(inv_site)]['micro_inverters'][self.inv_idx])
        df = df.fillna(-1)
        df['type'] = None
        df['type'] = np.where(df['energy.value'], 'inverter', df['type'])
        inverters = df[df['type'] == 'inverter'].reset_index(drop=True)
        # inverter string
        device_list = [inverters]
        for device in device_list:
            for idx, row in device.iterrows():
                inv_id = row['id']
                name = 'Inverter' + '-%s' % (idx+1)
                inv_serial = row['serial_number']
                inv_status = row['status']
                inv_kWh = row['energy.value']
                #inv_kW = row['power_produced']
                #address = row['type'] + '_%s' % (idx+1)
                inv_idx = '%s' % (idx)
                LOGGER.info('\nNodes\n\nname\n{name}\nID\n{inv_id}\nSerial\n{inv_serial}\nStatus\n{inv_status}\nkWh\n{inv_kWh}\nIndex\n{inv_idx}\n'.format(
                    name=name, inv_id=inv_id, inv_serial=inv_serial, inv_status=inv_status, inv_kWh=inv_kWh, inv_idx=inv_idx))  # , inv_kW=inv_kW ## \nkW\n{inv_kW}
                LOGGER.info(inv_kW)
                if inv_kW > 1:
                    self.setDriver('GV1', inv_kW)
                if inv_kW <= 1:
                    self.setDriver('GV1', 0)
                else:
                    pass
                LOGGER.info(inv_kWh)
                self.setDriver('GV2', inv_kWh)
                LOGGER.info(inv_serial)
                self.setDriver('GV3', inv_serial)
                LOGGER.info(inv_id)
                self.setDriver('GV5', inv_id)
                LOGGER.info(inv_status)
                normal1 = inv_status
                if normal1 == 'normal':
                    self.setDriver('GV4', 1)
                else:
                    self.setDriver('GV4', 0)

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def poll(self, polltype):
        pass
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            sleeptime = random.uniform(60, 240)
            sleep(sleeptime)
            LOGGER.info("sleeping is over")
            self.getpower(self)
            # self.reportDrivers()
        else:
            LOGGER.debug('longPoll (node)')

    def query(self, command):
        self.getpower(self)

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 119},
        {'driver': 'GV2', 'value': 0, 'uom': 33},
        {'driver': 'GV3', 'value': 0, 'uom': 56},
        {'driver': 'GV4', 'value': 0, 'uom': 25},
        {'driver': 'GV5', 'value': 0, 'uom': 56},
    ]

    id = 'inverter'

    commands = {
        'SITEINFO': query
    }
