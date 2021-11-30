import requests
import time
from devices_rules_test_station import *

RASBPI_IP_KRK = "10.10.13.144:8000"

MODESWITCH_HOME_SERVO_NO = 0
MODESWITCH_AWAY_SERVO_NO = 1
MODESWITCH_NIGHT_SERVO_NO = 2
MODESWITCH_VACATION_SERVO_NO = 3

CONTACTRON_SERVO_NO = 4
SDCO_SERVO_NO = 7

RELAY_SWITCH_HUB = 1
RELAY_SWITCH_R2 = 2
RELAY_SWITCH_IKEA_BULB = 8

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


def send_rasbpi_request(request, *args, sleep_time=5):
    print("Sending the request...")
    resp = request(*args)
    print("Status:" + str(resp.status_code))
    print("Resp:" + str(resp.json()))
    time.sleep(sleep_time)

#################################################### ALL MODES ##############################################

# NEEDS TO BE TESTED WITH THE REAL SETUP, THEN CAN BE REFACTORED FURTHER
request = requests.post
send_rasbpi_request(request, 'http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_HOME_SERVO_NO),
                                 headers=headers, data=data_mode_switch_home, sleep_time=6)


resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_HOME_SERVO_NO),
                                 headers=headers, data=data_mode_switch_home)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(5)

resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_NIGHT_SERVO_NO),
                                 headers=headers, data=data_mode_switch)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(5)

resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_AWAY_SERVO_NO),
                                 headers=headers, data=data_mode_switch)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(5)

resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_VACATION_SERVO_NO),
                                 headers=headers, data=data_mode_switch_vacation)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(5)


## MODE SWITCH INCLUDE ###

resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_HOME_SERVO_NO),
                                 headers=headers, data=data_mode_switch_include_home_btn)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(0.2)

resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, MODESWITCH_NIGHT_SERVO_NO),
                                 headers=headers, data=data_mode_switch_include_btn)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(5)


time.sleep(5)
#################################################### CONTACTRON ##############################################

resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, CONTACTRON_SERVO_NO),
                                 headers=headers, data=data_contactron)
print("Status:" + str(resp.status_code))
print("Resp:" + str(resp.json()))
time.sleep(16)


#################################################### HUB SWITCH ##############################################

resp = requests.get('http://{}/relays/{}'.format(RASBPI_IP_KRK, RELAY_SWITCH_HUB), headers=headers)

print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))
time.sleep(3)


resp = requests.post('http://{}/relays/{}/actions'.format(RASBPI_IP_KRK, RELAY_SWITCH_HUB),
                     headers=headers, data=str(hub_relay_reset))
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))

#################################################### FH FLAG ##############################################

for i in range(10):
    resp = response1 = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, 6),
                                     headers=headers, data=data_flag)
    time.sleep(1)
time.sleep(1)
time.sleep(6)

#################################################### IKEA BULB SWITCH ##############################################

resp = requests.get('http://{}/relays/{}'.format(RASBPI_IP_KRK, RELAY_SWITCH_IKEA_BULB), headers=headers)
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))
time.sleep(3)


resp = requests.post('http://{}/relays/{}/actions'.format(RASBPI_IP_KRK, RELAY_SWITCH_IKEA_BULB),
                     headers=headers, data=str(bulb_30s_reset))
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))

# inclusion mode:

resp = requests.post('http://{}/relays/{}/actions'.format(RASBPI_IP_KRK, RELAY_SWITCH_IKEA_BULB), headers=headers,
                     data=str(bulb_pairing))
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))


################################################### SDCO SWITCH ##############################################


resp = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, SDCO_SERVO_NO),
                     headers=headers, data=str(data_scdo_press))
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))
time.sleep(3)

resp = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, SDCO_SERVO_NO),
                     headers=headers, data=str(data_scdo_factory_reset))
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))

resp = requests.post('http://{}/servos/{}/actions'.format(RASBPI_IP_KRK, SDCO_SERVO_NO),
                     headers=headers, data=str(data_scdo_include))
print("Resp:" + str(resp.json()))
print("Status:" + str(resp.status_code))
time.sleep(3)
