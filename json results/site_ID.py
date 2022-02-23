import requests
import pandas as pd
import json
import numpy as np

# from file test
"""f = open('/Users/stevenbailey/UDI Development PG3/Nodeservers/udi-enphaseII-poly-master-v3/json results/owners-systems.json',)
# jsonData = open('snapshot.json',)  #json.loads(jsonData)
jsonData = json.load(f)"""

key = '33443540a4c162ed92df1c878e87867b'
user_id = '4d6a55794e7a55354d413d3d0a'

params = (('key', key), ('user_id', user_id))

response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems',  params=params).text  # for loop for solar array
#print('\n Inverters \n' + jsonData)
jsonData = json.loads(response)

print()
# print(jsonData['systems'][1])

df = pd.json_normalize(jsonData['systems'])
df = df.fillna(-1)

df['type'] = None
df['type'] = np.where(df['system_id'], 'system', df['type'])

system = df[df['type'] == 'system'].reset_index(drop=True)

# inverter string
device_list = [system]
for device in device_list:
    for idx, row in device.iterrows():
        id = row['system_id']
        id_new = id
        system_name = row['system_name']
        print('\n{id_new}\n\n{system_name}\n'.format(
            id_new=id_new, system_name=system_name))

print()
# print(df['id'])
print(df['system_id'])
print('\n')
print(df['system_name'])
print('\n')
# print(df['serial_number'])
# print(df['energy.value'])
# print(df['power_produced'])

# For file grab
# f.close()
