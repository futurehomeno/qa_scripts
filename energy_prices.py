# To do before start script: ssh -L 1883:localhost:1883  fh@10.10.30.211


import requests
import paho.mqtt.client as mqtt
import time
import json
import datetime

DELIVERY_AREA = 'NO5'
START_DAY = '2022-05-24T22:00:00Z'
URL_NORDPOOL = f'https://marketdata-api.nordpoolgroup.com/dayahead/prices/area?deliveryarea={DELIVERY_AREA}&status=O' \
               '&currency=NOK&startTime='

URL_LOGIN = 'https://marketdata.nordpoolgroup.com/oauth2/resourceownerpassword/acquiretoken'
LOGIN_DATA = {
    "apiId": "MarketData-Prices",
    "useTestUser": False,
    "username": "API_DATA_FUTUREHOME",
    "password": "wi14_miCNTmAN1)22"
}
# Prices scale
k = 10


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer " + self.token
        return r


# SCHEDULE_TOPIC = "pt:j1c1/mt:evt/rt:cloud/rn:energy_guard/ad:energy_price"
SCHEDULE_TOPIC = 'pt:j1/mt:evt/rt:app/rn:energy_guard/ad:1'
MQTT_HOST = 'localhost'


def configure_client(client):
    client.on_message = on_message
    print("Connecting to broker")
    if client.connect(MQTT_HOST) == 0:
        print("Connected")


def on_message(client, userdata, message):
    if message.topic == SCHEDULE_TOPIC:

        msg_str = str(message.payload.decode("utf-8"))
        msg = json.loads(msg_str)
        now = datetime.datetime.now()

        api_day = int(START_DAY[8:10])

        if now.day > api_day + 1:
            new_start_date = START_DAY.replace(str(api_day), str(now.day - 1))
            k_prices_list, time_list = sort_data_from_api(get_data(new_start_date))
        else:
            k_prices_list, time_list = sort_data_from_api(get_data(START_DAY))

        hours = now.hour
        if hours == 24:
            if msg['val']['price'] == k_prices_list[0] and msg['val']['from'].replace('+02:00', '').replace(str(hours),
                                                                                                            str(hours - 2)) == \
                    time_list[0]:
                print("PASS: Start time from Energy Report: ", msg['val']['from'], " Start time from Schedule",
                      time_list[hours])
                print("      Energy report: ", msg["val"]["price"], " Schedule: ", k_prices_list[0])
        elif hours == 25:
            if msg['val']['price'] == k_prices_list[1] and msg['val']['from'].replace('+02:00', '').replace(str(hours),
                                                                                                            str(hours - 2)) == \
                    time_list[1]:
                print("PASS: Start time from Energy Report: ", msg['val']['from'], " Start time from Schedule",
                      time_list[hours])
                print("      Energy report: ", msg["val"]["price"], " Schedule: ", k_prices_list[1])

        elif msg['val']['price'] == k_prices_list[hours] and msg['val']['from'].replace('+02:00', '').replace(
                str(hours), str(hours - 2)) == time_list[hours]:
            print("PASS: Start time from Energy Report: ", msg['val']['from'], " Start time from Schedule",
                  time_list[hours])
            print("      Energy report: ", msg["val"]["price"], " Schedule: ", k_prices_list[hours])
        else:
            print("FAIL: Start time from Energy Report: ", msg['val']['from'], " Start time from Schedule",
                  time_list[hours])
            print("      Energy report: ", msg["val"]["price"], " Schedule: ", k_prices_list[hours])


def get_data(start_time):
    access_token = requests.post(URL_LOGIN, json=LOGIN_DATA).json()['accessToken']

    headers = {
        "Authorization": f"Beareer {access_token}"
    }

    resp = requests.get(URL_NORDPOOL + start_time, auth=BearerAuth(access_token))

    return json.loads(resp.text)


def sort_data_from_api(response_info):
    prices_list = []
    time_list = []
    for price_info in response_info[0]['values']:
        prices_list.append(price_info['value'])

    for time_info in response_info[0]['values']:
        time_list.append(time_info['startTime'].replace('Z', ""))

    k_prices_list = [int(item / k) for item in prices_list]

    return k_prices_list, time_list


resp = get_data(START_DAY)

client = mqtt.Client("ScheduleTest")
configure_client(client)
client.loop_start()
client.subscribe(SCHEDULE_TOPIC)
print("Subscribing ", SCHEDULE_TOPIC)

# 24h long test
time.sleep(86400)
client.loop_stop()
