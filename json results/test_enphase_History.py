import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

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
#print(systemResponse["systems"][0]["status"])
#print('\n System ID \n', systemResponse["systems"][0]["system_id"])
#print('\n System ID \n', systemResponse["systems"][0]["system_id"])
#print('\n System Status \n', systemResponse["systems"][0]["status"])
#print('\n System Country \n', systemResponse["systems"][0]["country"])
hellohere = systemResponse["systems"][0]

print()
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

        print('\n{id_new}\n\n{system_name}\n'.format(
            id_new=id_new, system_name=system_name))

"""print()
# print(df['id'])
print(df['system_id'])
print('\n')
print(df['system_name'])
print('\n')
# print(df['serial_number'])
# print(df['energy.value'])
# print(df['power_produced'])"""


"""responseH = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=2527105',  params=params)  # 'https://api.enphaseenergy.com/api/v2/systems', # https://enlighten.enphaseenergy.com/app_user_auth/new?app_id=1409622241421 # https://api.enphaseenergy.com/api/v2/systems/[system_id]/stats
# https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=1409622241421
print(response)

presentday = datetime.now()
yesterday = presentday - timedelta(1)
second = presentday - timedelta(2)
third = presentday - timedelta(3)
fourth = presentday - timedelta(4)
fifth = presentday - timedelta(5)

start_date = yesterday.strftime('%Y-%m-%d')
end_date = presentday.strftime('%Y-%m-%d')
end_scnd = second.strftime('%Y-%m-%d')
end_tird = third.strftime('%Y-%m-%d')
end_four = fourth.strftime('%Y-%m-%d')
end_five = fourth.strftime('%Y-%m-%d')

print(start_date)
print(end_date)
print(end_scnd)
print(end_tird)


# 'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date=2021-11-10&end_date=2021-11-25'
# 'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?+start_date+end_date'
response2 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date='+start_date+'&end_date='+end_date,  params=params).text
print('\n Lifetime Energy Daily Report \n' + response2)
response3 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date='+end_scnd+'&end_date='+end_scnd,  params=params).text
print('\n Lifetime Energy Daily Report \n' + response3)
response4 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date='+end_tird+'&end_date='+end_tird,  params=params).text
print('\n Lifetime Energy Daily Report \n' + response4)
response5 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date='+end_four+'&end_date='+end_four,  params=params).text
print('\n Lifetime Energy Daily Report \n' + response5)
response6 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date='+end_five+'&end_date='+end_five,  params=params).text
print('\n Lifetime Energy Daily Report \n' + response6)
# gives 401 is no consumption meter
# response8 = requests.get(
#    'https://api.enphaseenergy.com/api/v2/systems/2527105/consumption_lifetimeconsumption_lifetime',  params=params).text
#print('\n rgm \n' + response8)"""
#### HISTORY ####
"""response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime',  params=params).text  # for loop for solar array
jsonData = json.loads(response)
print(jsonData)

#response = requests.get(response, params=params)
#print('\n Summary \n' + response)
Response = json.loads(response)
ystdy = len(Response['production'])-1
dybfo = len(Response['production'])-2
dybfy = len(Response['production'])-3
dybft = len(Response['production'])-4
dybf2 = len(Response['production'])-5
print('\nYesterday\n' + str(float(Response["production"][ystdy]/1000)))
print('\nSecond Day Before\n' + str(float(Response["production"][dybfo]/1000)))
print('\nThird Day Before\n' + str(float(Response["production"][dybfy]/1000)))
print('\nFourth Day Before\n' + str(float(Response["production"][dybft]/1000)))
print('\nFourth Day Before\n' + str(float(Response["production"][dybf2]/1000)))"""


#### HISTORY ####
response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/consumption_lifetime',  params=params).text  # for loop for solar array
jsonData = json.loads(response)
print(response)
print(jsonData)

#response = requests.get(response, params=params)
#print('\n Summary \n' + response) 
Response = json.loads(response)
ystdy = len(Response['consumption'])-1
dybfo = len(Response['consumption'])-2
dybfy = len(Response['consumption'])-3
dybft = len(Response['consumption'])-4
dybf2 = len(Response['consumption'])-5
print('\nYesterday\n' + str(float(Response["consumption"][ystdy]/1000)))
print('\nSecond Day Before\n' + str(float(Response["consumption"][dybfo]/1000)))
print('\nThird Day Before\n' + str(float(Response["consumption"][dybfy]/1000)))
print('\nFourth Day Before\n' + str(float(Response["consumption"][dybft]/1000)))
print('\nFourth Day Before\n' + str(float(Response["consumption"][dybf2]/1000)))
