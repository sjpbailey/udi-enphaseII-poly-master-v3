import requests
import pandas as pd
import json
import numpy as np

# from file test
"""f = open('/Users/stevenbailey/UDI Development PG3/Nodeservers/udi-enphaseII-poly-master-v3/json results/inverters.json',)
# jsonData = open('snapshot.json',)  #json.loads(jsonData)
jsonData = json.load(f)"""

key = '33443540a4c162ed92df1c878e87867b'
user_id = '4d6a55794e7a55354d413d3d0a'
system_id = '2527105'
# 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
system_id
inv_idx = 18
URL_SITE = 'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=' + \
    system_id + 'summary'
params = (('key', key), ('user_id', user_id))

r = requests.get(URL_SITE, params=params)
#LOGGER.info('\n Summary \n' + response)
print(r)

Response = json.loads(r.text)  # r.text
if (r.status_code == 200):
    # print(Response[0]['micro_inverters'][inv_idx]['energy']['value'])
    # print(Response[0]['micro_inverters'][inv_idx]['power_produced'])
    # print(int(Response[0]['micro_inverters'][inv_idx]['serial_number']))

    test_str = Response[0]['micro_inverters'][inv_idx]['serial_number']

# printing original string
    print("The original string is : " + test_str)

# Using string slicing
# Splitting string into equal halves
    res_first, res_second = test_str[:len(
        test_str)//2], test_str[len(test_str)//2:]

    first_chars = test_str[:7]
    last_chars = test_str[-5:]
    print(first_chars)
    print(last_chars)
# printing result
    #print("S/N first part : " + res_first)
    #print("S/N second part : " + res_second)

"""params = (('key', key), ('user_id', user_id))

response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=2527105',  params=params).text  # for loop for solar array
#print('\n Inverters \n' + jsonData)
jsonData = json.loads(response)"""

#print(Response)
# print(Response[0]['micro_inverters'][0]['id'])


# Response[0]['micro_inverters'][inv_idx]
# Use Line above to check each inverter one at a tiime
df = pd.json_normalize(Response[0]['micro_inverters'][inv_idx])  # [inv_idx]
df = df.fillna(-1)

df['type'] = None
df['type'] = np.where(df['energy.value'], 'inverter', df['type'])

inverters = df[df['type'] == 'inverter'].reset_index(drop=True)

# inverter string
device_list = [inverters]
for device in device_list:
    for idx, row in device.iterrows():
        inv_id = row['id']
        #id_new = id
        inv_serial = int(row['serial_number'])
        inv_status = row['status']
        inv_kWh = row['energy.value']
        inv_kW = row['power_produced.value']
        inv_idx = '%s' % (idx)
        print('\nID\n{inv_id}\nSN\n{inv_serial}\nStatus\n{inv_status}\nWh\n{inv_kWh}\nW\n{inv_kW}\nIDX\n{inv_idx}\n'.format(
            inv_id=inv_id, inv_serial=inv_serial, inv_status=inv_status, inv_kWh=inv_kWh/1000, inv_kW=inv_kW, inv_idx=inv_idx))  # inv_kW=inv_kW, ## \nW\n{inv_kW}
# GETS from Inverters
# inv_id = Response  # 0]['micro_inverters'][inv_idx]  # ['id']
#inv_serial = Response[0]['micro_inverters'][inv_idx]['serial_number']
#inv_stat = Response[0]['micro_inverters'][inv_idx]['status']
#inv_kWh = Response[0]['micro_inverters'][inv_idx]['energy']['value']
#inv_kW = Response[0]['micro_inverters'][inv_idx]['power_produced']
# print(Response[0]['micro_inverters'][inv_idx]['serial_number'])


"""df = pd.json_normalize(Response[0]['micro_inverters'])  # [inv_idx]
df = df.fillna(-1)

df['type'] = None
df['type'] = np.where(df['energy.value'], 'inverter', df['type'])

inverters = df[df['type'] == 'inverter'].reset_index(drop=True)

# inverter string
device_list = [inverters]
for device in device_list:
    for idx, row in device.iterrows():
        inv_id = row['id']
        #id_new = id
        #inv_serial = row['serial_number']
        inv_status = row['status']
        inv_kWh = row['energy.value']
        inv_kW = row['power_produced']
        inv_idx = '%s' % (idx)

        print('\n\nStatus\n{inv_status}\nWh\n{inv_kWh}\nW\n{inv_kW}\nIDX\n{inv_idx}\n'.format(
            inv_status=inv_status, inv_kWh=inv_kWh, inv_kW=inv_kW, inv_idx=inv_idx))

print(Response[int(idx)]['micro_inverters'][int(inv_idx)]['power_produced'])"""
# print(Response[0])
# print(inv_id)
# print(inv_serial)
# print(inv_stat)
# print(inv_kWh)
# print(inv_kW)
# print()

# print(inv_status)
# print(idx+1)
# print(df['id'])
# print(df['serial_number'])
# print(df['energy.value'])
# print(df['power_produced'])

# For file grab
# f.close()
