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

from nodes import EnphaseController
from nodes import EnphaseNode

LOGGER = udi_interface.LOGGER


class InverterNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, inv_id, inv_serial, inv_status, inv_kWh, inv_kW, inv_idx):
        super(InverterNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.inv_id = inv_id
        self.inv_serial = inv_serial
        self.inv_status = inv_status
        self.inv_kWh = inv_kWh
        self.inv_kW = inv_kW
        self.inv_idx = inv_idx

    def start(self):
        self.invertInfo(self)
        self.http = urllib3.PoolManager()

    def invertInfo(self, command):
        LOGGER.info('ID {}'.format(self.inv_id))
        self.setDriver('GV5', self.inv_id)
        LOGGER.info('kW {}'.format(float(self.inv_kW)/1000))
        self.setDriver('GV1', float(self.inv_kW)/1000)
        LOGGER.info('Wh {}'.format(float(self.inv_kWh)/1000))
        self.setDriver('GV2', float(self.inv_kWh)/1000)
        LOGGER.info('S/N {}'.format(self.inv_serial))
        self.setDriver('GV3', self.inv_serial)
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

    def poll(self, polltype):
        pass
        if 'shortPoll' in polltype:
            LOGGER.debug('shortPoll (node)')
            self.reportDrivers()
        else:
            pass
            #LOGGER.debug('longPoll (node)')

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 33},
        {'driver': 'GV2', 'value': 0, 'uom': 33},
        {'driver': 'GV3', 'value': 0, 'uom': 56},
        {'driver': 'GV4', 'value': 0, 'uom': 25},
        {'driver': 'GV5', 'value': 0, 'uom': 56},

    ]

    id = 'inverter'

    commands = {
        'SITEINFO': invertInfo

    }
