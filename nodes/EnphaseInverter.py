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

    # Randomly poll inverters to prevent API errors
    def start(self):
        self.http = urllib3.PoolManager()
        time.sleep(15)
        sleeptime = random.uniform(120, 360)
        sleep(sleeptime)
        LOGGER.info("sleeping is over")
        self.getpower(self)

    # GET Inverter Information
    def getpower(self, command):
        self.inv_idx = int(self.inv_idx)
        inv_site = int(0)
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
            self.system_id
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r2 = requests.get(URL_SITE, params=params)
            # LOGGER.info(r2)
            Response2 = r2.json() #json.loads(r2.text)
            if r2.status_code == 200:
                self.setDriver('ST', 1)
            else:
                self.setDriver('ST', 0)
            if r2.status_code == 409:
                LOGGER.info('You have EXCEEDED Your Monthly Hit Rate')
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
                inv_kW = row['power_produced.value']
                #address = row['type'] + '_%s' % (idx+1)
                inv_idx = '%s' % (idx)
                LOGGER.info('\nNodes\n\nname\n{name}\nID\n{inv_id}\nSerial\n{inv_serial}\nStatus\n{inv_status}\nkWh\n{inv_kWh}\nkW\n{inv_kW}\nIndex\n{inv_idx}\n'.format(
                    name=name, inv_id=inv_id, inv_serial=inv_serial, inv_status=inv_status, inv_kWh=inv_kWh, inv_kW=inv_kW, inv_idx=inv_idx))
                LOGGER.info(inv_kW)
                if inv_kWh > 1:
                    self.setDriver('GV1', float(inv_kW)/1000)
                if inv_kW <= 1:
                    self.setDriver('GV1', 0)
                else:
                    pass
                LOGGER.info(inv_kWh)
                self.setDriver('GV2', float(inv_kWh)/1000)
                LOGGER.info(inv_serial)
                first_chars = inv_serial[:5]
                LOGGER.info(first_chars)
                self.setDriver('GV3', first_chars)
                last_chars = inv_serial[-7:]
                LOGGER.info(last_chars)
                self.setDriver('GV6', last_chars)
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

    def query(self,command=None):
        self.reportDrivers()

    
    # NEED to do this: Do Not Poll unless you have power being produced  and 'GV1' != 0
    # Poll at random intervols
    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            sleeptime = random.uniform(60, 240)
            sleep(sleeptime)
            LOGGER.info("sleeping is over")
            self.getpower(self)
            # if 'GV1' == 0 start while loop, end while loop at sunrise
            #if 'GV1' == 0:
            #   self.reportDrivers() 
            #   start while loop:
            #   Wait for Sunrise
            #    self.getpower(self)
            
        else:
            LOGGER.debug('longPoll (node)')

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 33},
        {'driver': 'GV2', 'value': 0, 'uom': 33},
        {'driver': 'GV3', 'value': 0, 'uom': 56},
        {'driver': 'GV4', 'value': 0, 'uom': 25},
        {'driver': 'GV5', 'value': 0, 'uom': 56},
        {'driver': 'GV6', 'value': 0, 'uom': 56},
    ]

    id = 'inverter'

    commands = {
        'SITEINFO': getpower,
        'QUERY': query,
    }
