"""
Polyglot v3 node server Enphase
Copyright (C) 2021 Steven Bailey

MIT License
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import time
import logging
import pandas as pd
import numpy as np
import udi_interface

from nodes import EnphaseNode
from nodes import EnphaseInverter
from nodes import EnphaseMeter

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER
Custom = udi_interface.Custom
ISY = udi_interface.ISY

# IF you want a different log format than the current default
LOG_HANDLER.set_log_format(
    '%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')


class Controller(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(Controller, self).__init__(
            polyglot, primary, address, name)
        self.poly = polyglot
        self.name = 'Enphase Site Controller II'
        self.hb = 0
        self.Parameters = Custom(polyglot, 'customparams')
        self.Notices = Custom(polyglot, 'notices')
        self.TypedParameters = Custom(polyglot, 'customtypedparams')
        self.TypedData = Custom(polyglot, 'customtypeddata')
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.LOGLEVEL, self.handleLevelChange)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.ready()
        self.poly.addNode(self)
        self.default_key = "YourApiKey"
        self.default_user_id = "YourUser_id"

    def start(self, command=None):
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        #### Find Customer Sites ####
        self.customerSites(self)

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()

    def handleLevelChange(self, level):
        LOGGER.info('New log level: {}'.format(level))

    def delete(self):
        LOGGER.info('deleted.')

    def stop(self, command=None):
        LOGGER.debug('NodeServer stopped.')

    def set_module_logs(self, level):
        logging.getLogger('urllib3').setLevel(level)

    def check_params(self):
        self.Notices.clear()
        default_key = "YourApiKey"
        default_user_id = "YourUser_id"

        self.key = self.Parameters.key
        if self.key is None:
            self.key = default_key
            LOGGER.error(
                'check_params: key not defined in customParams, please add it.  Using {}'.format(default_key))
            self.key = default_key, self.user = self.Parameters.user

        self.user_id = self.Parameters.user_id
        if self.user_id is None:
            self.user_id = default_user_id
            LOGGER.error('check_params: user_id not defined in customParams, please add it.  Using {}'.format(
                default_user_id))
            self.user_id = default_user_id

        # Add a notice if they need to change the user/user_id from the default.
        if self.key == default_key or self.user_id == default_user_id:
            self.Notices['auth'] = 'Please set proper key and user_id in configuration page'
            self.setDriver('ST', 0)
        else:
            self.setDriver('ST', 1)

    #### Add Sites ####
    def customerSites(self, command):
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems'
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r = requests.get(URL_SITE, params=params)
            # LOGGER.info(r)
            Response = r.json() #json.loads(r.text)
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
        if r.status_code == 409:
            LOGGER.infor('You have EXCEEDED Your Monthly Hit Rate')
            time.sleep(66000)
            self.stop(self)
        else:
            # Add unix time for a poly restart "LOGER.info(datetime.utcfromtimestamp(1643673600).strftime('%c'))"
            ##{'reason': '409', 'message': ['Usage limit exceeded for plan Watt'], 'period': 'month', 'period_start': 1640995200, 'period_end': 1643673600, 'limit': 10000}
            pass

        if self.key != self.default_key:
            df = pd.json_normalize(Response['systems'])
            df = df.fillna(-1)
            df['type'] = None
            df['type'] = np.where(df['system_id'], 'system', df['type'])
            system = df[df['type'] == 'system'].reset_index(drop=True)
            # Add System Nodes (system string)
            device_list = [system]
            for device in device_list:
                for idx, row in device.iterrows():
                    name = row['system_name']
                    system_id = row['system_id']
                    LOGGER.info('\n{name}\n{system_id}\n'
                                .format(name=name, system_id=system_id))
                    LOGGER.info('SystemId {}' .format(system_id))
                    node = EnphaseNode.SiteNode(self.poly, self.address, 'site'+'_%s' % (idx+1), str(name), str(system_id), self.key, self.user_id)
                    self.poly.addNode(node)
        if system_id is not None:
            self.Inverters(self)
            self.setDriver('GV1', str(system_id))
        else:
            pass

    #### Add Inverters ####
    def Inverters(self, command):
        #### GET system_id ####
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems'
        params = (('key', self.key), ('user_id', self.user_id))
        try:
            r1 = requests.get(URL_SITE, params=params)

            # LOGGER.info(r1)
            Response1 = r1.json() #json.loads(r1.text)
        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))
        if r1.status_code == 409:
            LOGGER.infor('You have EXCEEDED Your Monthly Hit Rate')
            time.sleep(66000)
            self.stop(self)
        else:
            pass

        if self.key != self.default_key:
            df = pd.json_normalize(Response1['systems'])
            df = df.fillna(-1)
            df['type'] = None
            df['type'] = np.where(df['system_id'], 'system', df['type'])
            system = df[df['type'] == 'system'].reset_index(drop=True)
            # Add System Nodes (system string)
            device_list = [system]
            for device in device_list:
                for idx, row in device.iterrows():
                    name = row['system_name']
                    system_id = row['system_id']
                    LOGGER.info('\n{name}\n{system_id}\n'
                                .format(name=name, system_id=system_id))
                    LOGGER.info('SystemId {}' .format(system_id))
        if system_id is not None:
            system_id = str(system_id)
        #### GET Inverter Data ####
        URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
            system_id
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
        df['type'] = np.where(df['energy.value'], 'inverter', df['type'])
        inverters = df[df['type'] == 'inverter'].reset_index(drop=True)
        # inverter string
        if system_id is not None:
            device_list = [inverters]
            for device in device_list:
                for idx, row in device.iterrows():
                    inv_id = row['id']
                    name = 'Inverter' + '-%s' % (idx+1)
                    inv_serial = row['serial_number']
                    inv_status = row['status']
                    inv_kWh = row['energy.value']
                    inv_kW = row['power_produced.value']
                    address = row['type'] + '_%s' % (idx+1)
                    inv_idx = '%s' % (idx)
                    LOGGER.info('\nDiscovered by Controller\n\nID\n{inv_id}\nSerial\n{inv_serial}\nStatus\n{inv_status}\nkWh\n{inv_kWh}\nkW\n{inv_kW}\nIndex\n{inv_idx}\n'.format(
                        inv_id=inv_id, inv_serial=inv_serial, inv_status=inv_status, inv_kWh=inv_kWh, inv_kW=inv_kW, inv_idx=inv_idx)) 
                    node = EnphaseInverter.InverterNode(
                        self.poly, self.address, address, name, str(system_id), self.key, self.user_id, inv_idx=inv_idx,)
                    self.poly.addNode(node)

        #### Get Consumption Meter ####
        if system_id is not None:
            URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/' + \
                system_id + '/consumption_stats'
            params = (('key', self.key), ('user_id', self.user_id))
            try:
                r = requests.get(URL_SITE, params=params)
                LOGGER.info(r)
                jsonResponse = r.json() #json.loads(r.text)
            except requests.exceptions.RequestException as e:
                LOGGER.error("Error: " + str(e))
            if r.status_code == 401:
                LOGGER.info("Consumption Meter not found 'None'")
            if r != 401:
                LOGGER.info("Consumption Meter found")
            address = 'Meter_1'
            name = 'Meter 1'
            #if r == 200:
            if r.status_code == 200:
                df = pd.json_normalize(jsonResponse['intervals'][0])
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
                        LOGGER.info('\nReport Time\n{id_new}\n\nDevice\n{device}\nkWh\n{kwh}\n\nIndex\n{mtr_idx}\n'.format(
                        id_new=id_new, device=device, kwh=kwh, mtr_idx=mtr_idx))
            
                        node = EnphaseMeter.MeterNode(self.poly, self.address, 'meter'+'_%s' % (idx+1), 'Consumption Meter', str(system_id), self.key, self.user_id)
                        self.poly.addNode(node)

    def remove_notices_all(self, command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.Notices))
        # Remove all existing notices
        self.Notices.clear()

    id = 'ctl'

    commands = {
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'SITEINFO': Inverters,
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 1, 'uom':56}

    ]
