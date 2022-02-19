import requests
import json
import datetime
from datetime import datetime, timedelta
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

response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=2527105',  params=params)  # 'https://api.enphaseenergy.com/api/v2/systems', # https://enlighten.enphaseenergy.com/app_user_auth/new?app_id=1409622241421 # https://api.enphaseenergy.com/api/v2/systems/[system_id]/stats
# https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=1409622241421
# print(response)

presentday = datetime.now()
yesterday = presentday - timedelta(1)
second = presentday - timedelta(2)
third = presentday - timedelta(3)

start_date = yesterday.strftime('%Y-%m-%d')
end_date = presentday.strftime('%Y-%m-%d')
end_scnd = second.strftime('%Y-%m-%d')
end_tird = third.strftime('%Y-%m-%d')
start_date = start_date
end_date = end_date

# yesterday = (datetime.datetime.now() +
#             datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
# two_days_ago = (datetime.datetime.now() +
#                datetime.timedelta(days=-2)).strftime('%Y-%m-%d')

# 'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?start_date=2021-11-10&end_date=2021-11-25'
# 'https://api.enphaseenergy.com/api/v2/systems/2527105/energy_lifetime?+start_date+end_date'


# gives 401 is no consumption meter or {"reason":"404","message":["Resource not found"]}
response9 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/consumption_lifetime',  params=params).text
print('\n Consumption Meter Life Time\n' + response9)
print(response9)
if response9[0] == 401:
    print('False')
#for i in response9:
#    print(i)
#for key in response9:
#    print(key)

# {"message":"The given system does not contain any active and enabled consumption meter"}


"""URL_SITE = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/consumption_stats', params=params).text
r = requests.get(URL_SITE, params=params)

print('\n Consumption Meter Stats \n' + r)"""

# if response8 is None:
#    print('False')
# if response8 is None:
#    print('True')

# Customers Systems = system_id
# for loop looking at system id to add Systems

"""response3 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems', params=params).text  # params=params
# print(response3)
systemResponse = json.loads(response3)
print(systemResponse["systems"][0]["status"])
print('\n System ID \n', systemResponse["systems"][0]["system_id"])
#print('\n System Status \n', systemResponse["systems"][0]["status"])
#print('\n System Country \n', systemResponse["systems"][0]["country"])
#hellohere = systemResponse["systems"][0]"""

#print('\n Str Found \n {} sites'.format(hellohere))
# print(hellohere["system_id"])
#howlong = len(hellohere["system_id"])
# print(howlong)
# for i in hellohere:
#    print('\n', i,  hellohere[i])

#'system_id' in hellohere.values()
#print(i, hellohere[i])

# energy_lifetime?start_date=2013-01-01&end_date=2013-01-06

#### Consumption Meter? ####
# GET https://api.enphaseenergy.com/api/v2/systems/66/production_meter_readings?end_at=1473901755
#response10 = requests.get(
#    'https://api.enphaseenergy.com/api/v2/systems/2527105/production_meter_readings',  params=params).text
#print('\n production meter \n' + response10)


response11 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/consumption_lifetime',  params=params).text
print('\n consumption lifetime \n' + response11)
#consumption_lifetime
print('\n System kW \n', response11[0])

# consumption_lifetime - {"reason":"401","message":["Not authorized to access requested resource"]}
# consumption_stats - {"message":"The given system does not contain any active and enabled consumption meter"}
response8 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/consumption_stats',  params=params).text  # consumption_lifetime
print('\n consumption meter \n' + response8)


"""response4 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/inventory',  params=params).text
print('\n Equipmet Inventory \n' + response4)"""

"""response5 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/2527105/stats?datetime_format=iso8601',  params=params).text
print('\n Equipment Stats \n' + response5)"""

"""response6 = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site?site_id=2527105',  params=params).text  # for loop for solar array
print('\n Inverters \n' + response6)
# for i in response6["micro_inverters"]:  # inverter_summary
#    inverters = str(["micro_inverters"])
#    print(inverters)    # inverter"""

"""system_id = '2527105'
response = requests.get(
    'https://api.enphaseenergy.com/api/v2/systems/' + system_id + '/summary',  params=params)
#print('\n Summary \n' + response)
jsonResponse = json.loads(response.text)

# print(response.text.encode('utf8'))
print('\n System kW \n', jsonResponse["current_power"])
print('\n System kWh \n', jsonResponse["energy_today"]/1000)
print('\n System Status \n', jsonResponse["status"])
print('\n System kWh Today\n', jsonResponse["energy_today"]/1000)
print('\n System kWh Life Time\n', jsonResponse["energy_lifetime"]/1000)"""

# print(int(jsonResponse["current_power"]))

# print(response3["system_id"])
# for key, value in response7:
#    print(value)


# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://api.enphaseenergy.com/api/v2/systems/67/summary?key=APPLICATION-API-KEY&user_id=ENLIGHTEN-USERID')
