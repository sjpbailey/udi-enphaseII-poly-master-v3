"""
Polyglot v3 node server Enphase
Copyright (C) 2021 Steven Bailey

MIT License
"""

import udi_interface
from datetime import datetime, timedelta
import json
import urllib3
import logging
import pandas as pd
import numpy as np
import os
import requests
from requests.auth import HTTPBasicAuth  # HTTP

from nodes import EnphaseNode

LOGGER = udi_interface.LOGGER


class InverterNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, inv_id, inv_serial, inv_status, inv_kWh, inv_kW):
        super(InverterNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        # apikey = os.environ.get("apikey")
        self.inv_id = inv_id
        self.inv_serial = inv_serial
        self.inv_status = os.environ.get(inv_status)
        self.inv_kWh = inv_kWh
        self.inv_kW = inv_kW

    def start(self):
        self.invertInfo(self)
        self.http = urllib3.PoolManager()

    def invertInfo(self, command):
        id = self.inv_id
        status = self.inv_status
        kW = self.inv_kW
        LOGGER.info('ID {}'.format(self.inv_id))
        self.setDriver('GV5', id)  # int(self.inv_id), report=True
        LOGGER.info('kW {}'.format(float(kW)))
        self.setDriver('GV1', float(self.inv_kW))
        LOGGER.info('Wh {}'.format(float(self.inv_kWh)))
        self.setDriver('GV2', '{}'.format(float(self.inv_kWh)))
        LOGGER.info('S/N {}'.format(self.inv_serial))
        self.setDriver('GV3', int(self.inv_serial))
        LOGGER.info('STATUS {}'.format(status))
        normal1 = self.inv_status
        LOGGER.info(normal1)
        if normal1 == 'normal':
            self.setDriver('GV4', 1)
        else:
            self.setDriver('GV4', 0)
        if status is not None:
            self.setDriver('ST', 1)
        else:
            self.setDriver('ST', 0)
        pass

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.reportDrivers()
        else:
            self.invertInfo(self)
            LOGGER.debug('longPoll (node)')

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 30},
        {'driver': 'GV2', 'value': 0, 'uom': 33},
        {'driver': 'GV3', 'value': 0, 'uom': 56},
        {'driver': 'GV4', 'value': 0, 'uom': 25},
        {'driver': 'GV5', 'value': 0, 'uom': 56},

    ]

    id = 'invert'

    commands = {
        'SITEINFO': invertInfo

    }
