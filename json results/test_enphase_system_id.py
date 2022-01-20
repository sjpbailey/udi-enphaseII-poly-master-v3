import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from numpy import random
from time import sleep

sleeptime = random.uniform(2, 4)
print("sleeping for:", sleeptime, "seconds")
sleep(sleeptime)
print("sleeping is over")

# System ID:2527105
# url auth? 1409622241421

key = '33443540a4c162ed92df1c878e87867b'
user_id = '4d6a55794e7a55354d413d3d0a'

params = (('key', key), ('user_id', user_id))
#('key', '33443540a4c162ed92df1c878e87867b'),  # 4d6a55794e7a55354d413d3d0a #
# ('user_id', '4d6a55794e7a55354d413d3d0a'),  # 4d6a55794e7a55354d413d3d0a
# )

#### System Status Site ID ####
response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems',  params=params).text  # for loop for solar array
#print('\n Inverters \n' + jsonData)
jsonData = json.loads(response)
systemResponse = json.loads(response)
# print(systemResponse["systems"][0]["status"])
#print('\n System ID \n', systemResponse["systems"][0]["system_id"])
#print('\n System ID \n', systemResponse["systems"][0]["system_id"])
#print('\n System Status \n', systemResponse["systems"][0]["status"])
#print('\n System Country \n', systemResponse["systems"][0]["country"])
hellohere = systemResponse["systems"][0]
# print(hellohere)
#### Iter Response ####
df = pd.json_normalize(jsonData['systems'])
df = df.fillna(-1)

df['type'] = None
df['type'] = np.where(df['system_id'], 'system', df['type'])
system = df[df['type'] == 'system'].reset_index(drop=True)
# System string
device_list = [system]
for device in device_list:
    for idx, row in device.iterrows():
        id = row['system_id']
        id_new = id
        system_name = row['system_name']
        system_public_name = row['system_public_name']
        status = row['status']
        timezone = row['timezone']
        print('\nSystem ID\n{id_new}\n\nSystem Name\n{system_name}\n\nType\n{system_public_name}\n''\nstatus ID\n{status}\n'.format(
            id_new=id_new, system_name=system_name, system_public_name=system_public_name, status=status))

"""print()
# print(df['id'])
print(df['system_id'])
print('\n')
print(df['system_name'])
print('\n')
# print(df['serial_number'])
# print(df['energy.value'])
# print(df['power_produced'])"""
