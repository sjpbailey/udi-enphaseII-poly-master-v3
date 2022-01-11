import requests
import json
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


"""params = (
    ('key', '33443540a4c162ed92df1c878e87867b'),  # 4d6a55794e7a55354d413d3d0a #
    ('user_id', '4d6a55794e7a55354d413d3d0a'),  # 4d6a55794e7a55354d413d3d0a
)

response = requests.get(
    'https://enlighten.enphaseenergy.com/app_user_auth/new?app_id=1409622241421',  params=params)  # 'https://api.enphaseenergy.com/api/v2/systems', # https://enlighten.enphaseenergy.com/app_user_auth/new?app_id=1409622241421 # https://api.enphaseenergy.com/api/v2/systems/[system_id]/stats

print(response)"""


#f = open('/Users/stevenbailey/UDI Development PG3/Nodeservers/udi-enphaseII-poly-master-v3/json results/owners-systems.json',)
# jsonData = open('snapshot.json',)  # json.loads(jsonData)
f = open('//Users/stevenbailey/UDI Development PG3/Nodeservers/udi-enphaseII-poly-master-v3/json results/lifetime-consumption-report.json',)
jsonResponse = json.load(f)
print(jsonResponse['consumption'][5])
if jsonResponse['consumption'][0] is not None:
    print('meter up')


#system_id = '2527105'
"""response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems', params=params)  # + system_id +
#print('\n Summary \n' + response)
jsonResponse = json.loads(response.text)"""

# print(jsonResponse)
"""print(jsonResponse["system"][0]["system_id"])  # [0]["system_id"])

df = pd.json_normalize(jsonResponse['systems'])
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
        address = 'Site' + '-%s' % (idx+1)
        print('\n{name}\n{system_id}\n{address}\n'.format(name=name, system_id=system_id, address=address)
              )"""


# print(response.text.encode('utf8'))
#print('\n System kW \n', jsonResponse["current_power"])
#print('\n System kWh \n', jsonResponse["energy_today"]/1000)
#print('\n System Status \n', jsonResponse["status"])
#print('\n System kWh Today\n', jsonResponse["energy_today"]/1000)
#print('\n System kWh Life Time\n', jsonResponse["energy_lifetime"]/1000)

# print(int(jsonResponse["current_power"]))

# print(jsonResponse)
# for i in jsonResponse["systems"][0]:
#    print(i, " : ", jsonResponse[i])
# for key, value in jsonResponse["systems"]:
#   print(value)

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://api.enphaseenergy.com/api/v2/systems/67/summary?key=APPLICATION-API-KEY&user_id=ENLIGHTEN-USERID')
# For file grab
f.close()
