import pandas as pd
import json
import numpy as np

f = open('/Users/stevenbailey/UDI Development PG3/Nodeservers/udi-enphaseII-poly-master-v3/json results/inverters.json',)
# jsonData = open('snapshot.json',)  #json.loads(jsonData)
jsonData = json.load(f)

print()
print(jsonData[0]['micro_inverters'][1])

df = pd.json_normalize(jsonData[0]['micro_inverters'])
df = df.fillna(-1)

df['type'] = None
df['type'] = np.where(df['energy.value'], 'inverter', df['type'])

inverters = df[df['type'] == 'inverter'].reset_index(drop=True)

# inverter string
device_list = [inverters]
for device in device_list:
    for idx, row in device.iterrows():
        id = row['id']
        id_new = id
        serial = row['serial_number']
        kWh = row['energy.value']
        kW = row['power_produced']
        print('\n{id_new}\n{serial}\n{kWh}\n{kW}\n'.format(
            id_new=id_new, serial=serial, kWh=kWh, kW=kW))

"""print()
print(df['id'])
print(df['serial_number'])
print(df['energy.value'])
print(df['power_produced'])"""


f.close()
