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
#from nodes import EnphaseInverter

LOGGER = udi_interface.LOGGER


class MeterNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, system_id, key, user_id):
        super(MeterNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.name = name
        self.system_id = system_id
        self.key = key
        self.user_id = user_id
        

    def start(self):
        self.meterInfo(self)
        self.http = urllib3.PoolManager()

    #### Get Current consumption ####
    def meterInfo(self, command):
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/' + \
            self.system_id + '/consumption_stats'
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r = requests.get(URL_SITE, params=params)
            Response = r.json() #loads(r.text)
            LOGGER.info(r.status_code)
            if r.status_code == 200:
                self.setDriver('ST', 1)
            else:
                self.setDriver('ST', 0)
                
            
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))    

        #### Iter Response ####
        df = pd.json_normalize(Response['intervals'][0])
        df = df.fillna(-1)

        df['type'] = None
        df['type'] = np.where(df['end_at'], 'system', df['type'])
        system = df[df['type'] == 'system'].reset_index(drop=True)
        # System string
        device_list = [system]
        for device in device_list:
            for idx, row in device.iterrows():
                id = row['end_at']
                id_new = id
                device = row['devices_reporting']
                kwh = row['enwh']
                mtr_idx = '%s' % (idx)
                print('\nReport Time\n{id_new}\n\nDevice\n{device}\nkWh\n{kwh}\n\nIndex\n{mtr_idx}\n'.format(
                    id_new=id_new, device=device, kwh=kwh, mtr_idx=mtr_idx))
            
                LOGGER.info(kwh/100)
                self.setDriver('GV1', float(kwh)/100)
                self.meterHist(self)

    #### Get History ####
    def meterHist(self, command, **kwargs):
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/' + \
            self.system_id + '/consumption_lifetime'
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r = requests.get(URL_SITE, params=params, **kwargs)
            #print('\n Summary \n' + r)
            Response = json.loads(r.text)
            ystdy = len(Response['consumption'])-1
            dybfo = len(Response['consumption'])-2
            dybfy = len(Response['consumption'])-3
            dybft = len(Response['consumption'])-4
            dybf2 = len(Response['consumption'])-5
            LOGGER.info(Response['consumption'][ystdy]/1000)  # Yesterday
            self.setDriver('GV2', float(Response["consumption"][ystdy]/1000))
            LOGGER.info(Response['consumption'][dybfo]/1000)  # Two Days Ago
            self.setDriver('GV3', float(Response["consumption"][dybfo]/1000))
            LOGGER.info(Response['consumption'][dybfy]/1000)  # Three Days Ago
            self.setDriver('GV4', float(Response["consumption"][dybfy]/1000))
            LOGGER.info(Response['consumption'][dybft]/1000)  # Four Days Ago
            self.setDriver('GV5', float(Response["consumption"][dybft]/1000))
            LOGGER.info(Response['consumption'][dybf2]/1000)  # Five Days Ago
            self.setDriver('GV6', float(Response["consumption"][dybf2]/1000))
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))

    def query(self,command=None):
        self.reportDrivers()

    # Do Not Poll unless you have power being produced
    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.meterInfo(self)
        else:
            LOGGER.debug('longPoll (node)')

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 30},
        {'driver': 'GV2', 'value': 0, 'uom': 33},
        {'driver': 'GV3', 'value': 0, 'uom': 33},
        {'driver': 'GV4', 'value': 0, 'uom': 33},
        {'driver': 'GV5', 'value': 0, 'uom': 33},
        {'driver': 'GV6', 'value': 0, 'uom': 33},
    ]

    id = 'meter'

    commands = {
        'SITEINFO': meterInfo,
        'QUERY': query,

    }
