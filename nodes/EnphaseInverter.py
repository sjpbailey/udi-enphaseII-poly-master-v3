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
import logging
import pandas as pd
import numpy as np
import requests
from requests.auth import HTTPBasicAuth  # HTTP

from nodes import EnphaseController
from nodes import EnphaseNode

LOGGER = udi_interface.LOGGER


class InverterNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, system_id, key, user_id, inv_idx, ):
        super(InverterNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        # self.inv_id = inv_id
        # self.inv_serial = inv_serial
        # self.inv_status = inv_status
        self.system_id = system_id
        self.key = key
        self.user_id = user_id
        self.inv_idx = int(inv_idx)

    def start(self):
        self.http = urllib3.PoolManager()
        self.getpower(self)

    """def invertInfo(self, command):
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
            time.sleep(10)
            self.getpower(self)
        else:
            self.setDriver('ST', 0)
            pass"""

    #### GET Inverter Data ####
    def getpower(self, command):
        self.inv_idx = int(self.inv_idx)
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
            self.system_id
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r2 = requests.get(URL_SITE, params=params)
            # LOGGER.info(r2)
            Response2 = json.loads(r2.text)
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
        #### Sort Inverter Data ####
        df = pd.json_normalize(Response2[0]['micro_inverters'])
        df = df.fillna(-1)
        df['type'] = None
        df['type'] = np.where(df['energy.value'],
                              'inverter', df['type'][self.inv_idx])
        inverters = df[df['type'] == 'inverter'].reset_index(drop=True)
        # inverter string
        if self.system_id is not None:
            device_list = [inverters]
            for device in device_list:
                for idx, row in device.iterrows():
                    inv_id = row['id']
                    name = 'Inverter' + '-%s' % (idx+1)
                    inv_serial = row['serial_number']
                    inv_status = row['status']
                    inv_kWh = row['energy.value']
                    inv_kW = row['power_produced']
                    address = row['type'] + '_%s' % (idx+1)
                    inv_idx = '%s' % (idx)
                    LOGGER.info('\nID\n{inv_id}\nSerial\n{inv_serial}\nStatus\n{inv_status}\nkWh\n{inv_kWh}\nkW\n{inv_kW}\nIndex\n{inv_idx}\n'.format(
                        inv_id=inv_id, inv_serial=inv_serial, inv_status=inv_status, inv_kWh=inv_kWh, inv_kW=inv_kW, inv_idx=inv_idx))
                    LOGGER.info(inv_kW)
                    self.setDriver('GV1', inv_kW)

            """if (r.status_code == 200):
                #LOGGER.info('Energy values are currently present')
                # LOGGER.info('kW {}'.format(
                #    response[0]['micro_inverters'][int(self.inv_idx)]['power_produced'])/100)
                self.setDriver('GV1', response[0]['micro_inverters'][int(
                    self.inv_idx)]['power_produced'])
                # LOGGER.info('Wh {}'.format(
                #    response[0]['micro_inverters'][int(self.inv_idx)]['energy']['value']/1000))
                self.setDriver('GV2', response[0]['micro_inverters'][int(
                    self.inv_idx)]['energy']['value']/1000)
                # LOGGER.info('ID {}'.format(
                #    (response[0]['micro_inverters'][int(self.inv_idx)]['id'])))
                self.setDriver(
                    'GV5', response[0]['micro_inverters'][int(self.inv_idx)]['id'])
                # LOGGER.info(
                #    'S/N {}'.format((response[0]['micro_inverters'][int(self.inv_idx)]['serial_number'])))
                self.setDriver('GV3', response[0]['micro_inverters'][int(
                    self.inv_idx)]['serial_number'])
                # LOGGER.info('STATUS {}'.format(
                #    (response[0]['micro_inverters'][int(self.inv_idx)]['status'])))
                # LOGGER.info(self.inv_status)
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
            LOGGER.info(self.inv_idx)"""

    def poll(self, polltype):
        pass
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.getpower(self)
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
