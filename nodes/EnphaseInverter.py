"""
Polyglot v3 node server Enphase
Copyright (C) 2021 Steven Bailey

MIT License
"""

import udi_interface
from datetime import datetime, timedelta
import time
import json
import urllib3
import logging
import pandas as pd
import numpy as np
import requests
from requests.auth import HTTPBasicAuth  # HTTP

from nodes import EnphaseController
from nodes import EnphaseNode

LOGGER = udi_interface.LOGGER


class InverterNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, system_id, key, user_id, inv_id, inv_serial, inv_status,  inv_idx, ):
        #inv_kWh, inv_kW,
        super(InverterNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.inv_id = inv_id
        self.inv_serial = inv_serial
        self.inv_status = inv_status
        #self.inv_kWh = inv_kWh
        #self.inv_kW = inv_kW
        self.inv_idx = inv_idx
        self.system_id = system_id
        self.key = key
        self.user_id = user_id

    def start(self):
        self.invertInfo(self)
        time.sleep(130)
        self.getpower(self)
        #self.http = urllib3.PoolManager()

    def invertInfo(self, command):
        LOGGER.info('ID {}'.format(self.inv_id))
        self.setDriver('GV5', self.inv_id)  # ID
        LOGGER.info('S/N {}'.format(self.inv_serial))
        self.setDriver('GV3', self.inv_serial)  # Serial Number
        LOGGER.info('STATUS {}'.format(self.inv_status))
        LOGGER.info(self.inv_status)
        if self.inv_status == 'normal':
            self.setDriver('GV4', 1)
        else:
            self.setDriver('GV4', 0)
        if self.inv_status is not None:
            self.setDriver('ST', 1)
        else:
            self.setDriver('ST', 0)
            pass

        #### GET Inverter Data ####
    def getpower(self, command):
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
            self.system_id
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r = requests.get(URL_SITE, params=params)
            Response = json.loads(open(r.text))
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
            LOGGER.info(self.inv_idx)
        #### Sort Inverter Status ####
        df = pd.json_normalize(
            Response[0]['micro_inverters'][int(self.inv_idx)])
        df = df.fillna(-1)
        df['type'] = None
        df['type'] = np.where(df['energy.value'], 'inverter', df['type'])
        inverters = df[df['type'] == 'inverter'].reset_index(drop=True)
        # inverter string
        if self.system_id is not None:
            device_list = [inverters]
            for device in device_list:
                for idx, row in device.iterrows():
                    inv_status = row['status']
                    inv_kWh = row['energy.value']
                    inv_kW = row['power_produced']
                    LOGGER.info('\n{inv_status}\n{inv_kWh}\n{inv_kW}\n'.format(
                        inv_kWh=inv_kWh, inv_kW=inv_kW, inv_status=inv_status))
                else:
                    pass
                LOGGER.info('kW {}'.format(float(inv_kW)))  # kW
                self.setDriver('GV1', float(inv_kW))  # kW
                LOGGER.info('Wh {}'.format(float(inv_kWh)/1000))
                self.setDriver('GV2', float(inv_kWh)/1000)  # kWh

    def poll(self, polltype):
        pass
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.getpower(self)
        else:
            LOGGER.debug('longPoll (node)')

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
        'SITEINFO': getpower
    }
