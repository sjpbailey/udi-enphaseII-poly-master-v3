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
from nodes import EnphaseInverter

LOGGER = udi_interface.LOGGER


class SiteNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, system_id, key, user_id):
        super(SiteNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.name = name
        self.system_id = system_id
        self.key = key
        self.user_id = user_id

    def start(self):
        self.siteInfo(self)
        self.http = urllib3.PoolManager()

    #### Get Current Production ####
    def siteInfo(self, command):
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/' + \
            self.system_id + '/summary'
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r = requests.get(URL_SITE, params=params)

            Response = r.json() #json.loads(r.text) #Response1 = r1.json()
            LOGGER.info(Response["current_power"])
            self.setDriver('GV1', str(Response["current_power"]/1000))
            LOGGER.info(Response["energy_today"])
            self.setDriver('GV2', float(Response["energy_today"]/1000))
            LOGGER.info(Response["energy_lifetime"])
            self.setDriver('GV3', float(Response["energy_lifetime"]/1000))
            LOGGER.info(Response["modules"])
            self.setDriver('GV10', str(Response['modules']))
            kw1 = float(Response["current_power"]/1000)
            kw2 = float(kw1*1000)
            kw3 = float(kw2//220)
            LOGGER.info(kw3)
            self.setDriver('GV11', float(kw3), report=True, force=True)
            LOGGER.info(Response["status"])
            normal1 = Response["status"]
            if normal1 == 'normal':
                self.setDriver('GV4', 1)
                self.siteHist(self)
            else:
                self.setDriver('GV4', 0)
            if r.status_code == 200:
                self.setDriver('ST', 1)
            else:
                self.setDriver('ST', 0)
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))

    #### Get History ####
    def siteHist(self, command):
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/' + \
            self.system_id + '/energy_lifetime'
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r = requests.get(URL_SITE, params=params)
            #print('\n Summary \n' + r)
            Response = r.json() #json.loads(r.text)
            ystdy = len(Response['production'])-1
            dybfo = len(Response['production'])-2
            dybfy = len(Response['production'])-3
            dybft = len(Response['production'])-4
            dybf2 = len(Response['production'])-5
            LOGGER.info(Response['production'][ystdy]/1000)  # Yesterday
            self.setDriver('GV5', float(Response["production"][ystdy]/1000))
            LOGGER.info(Response['production'][dybfo]/1000)  # Two Days Ago
            self.setDriver('GV6', float(Response["production"][dybfo]/1000))
            LOGGER.info(Response['production'][dybfy]/1000)  # Three Days Ago
            self.setDriver('GV7', float(Response["production"][dybfy]/1000))
            LOGGER.info(Response['production'][dybft]/1000)  # Four Days Ago
            self.setDriver('GV8', float(Response["production"][dybft]/1000))
            LOGGER.info(Response['production'][dybf2]/1000)  # Five Days Ago
            self.setDriver('GV9', float(Response["production"][dybf2]/1000))
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))

    def query(self,command=None):
        self.reportDrivers()

    # Do Not Poll unless you have power being produced
    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.siteInfo(self)
            #if 'GV1' != 0:
            #    self.siteInfo(self)
            #if 'GV1' == 0:
            #    self.reportDrivers()    
        else:
            LOGGER.debug('longPoll (node)')

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 30},
        {'driver': 'GV2', 'value': 0, 'uom': 33},
        {'driver': 'GV3', 'value': 0, 'uom': 33},
        {'driver': 'GV4', 'value': 0, 'uom': 25},
        {'driver': 'GV5', 'value': 0, 'uom': 33},
        {'driver': 'GV6', 'value': 0, 'uom': 33},
        {'driver': 'GV7', 'value': 0, 'uom': 33},
        {'driver': 'GV8', 'value': 0, 'uom': 33},
        {'driver': 'GV9', 'value': 0, 'uom': 33},
        {'driver': 'GV10', 'value': 0, 'uom': 56},
        {'driver': 'GV11', 'value': 0.01, 'uom': 1},
    ]

    id = 'site'

    commands = {
        'SITEINFO': siteInfo,
        'QUERY': query,

    }
