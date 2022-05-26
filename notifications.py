import paho.mqtt.client as mqtt
import time

MQTT_HOST = 'localhost'

SDCO_ADDRESS = '22_0'
MOTION_SENSOR_ADDRESS = '28_0'
OPEN_SENSOR = '3_1'
WATER_SENSOR = '5_1'

FIREALARM_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:alarm_fire/ad:{}'.format(SDCO_ADDRESS)
TEMPERATURE_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:sensor_temp/ad:{}'.format(SDCO_ADDRESS)
TAMPERING_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:alarm_burglar/ad:{}'.format(SDCO_ADDRESS)
BATTERY_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:battery/ad:{}'.format(SDCO_ADDRESS)
MOTION_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:sensor_presence/ad:{}'.format(MOTION_SENSOR_ADDRESS)
OPENED_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:sensor_contact/ad:{}'.format(OPEN_SENSOR)
WATERLEAK_TOPIC = 'pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:alarm_water/ad:{}'.format(WATER_SENSOR)

SDCO_FIREALARM_MSG = {
  "ctime": "2020-07-01T13:40:29+0200",
  "props": {},
  "serv": "alarm_fire",
  "tags": [],
  "type": "evt.alarm.report",
  "val": {
    "event": "smoke",
    "status": "activ"
  },
  "val_t": "str_map"
}

SDCO_TEMP_MSG = {
  "ctime": "2021-02-19T14:31:51+0100",
  "props": {
    "unit": "C"
  },
  "serv": "sensor_temp",
  "tags": [],
  "type": "evt.sensor.report",
  "val": 22,
  "val_t": "float"
}

TAMPERING_MSG = {
  "ctime": "2020-07-01T13:40:29+0200",
  "props": {},
  "serv": "alarm_burglar",
  "tags": [],
  "type": "evt.alarm.report",
  "val": {
    "event": "tamper_removed_cover",
    "status": "activ"
  },
  "val_t": "str_map"
}

SDCO_BATTERY_MSG = {
  "ctime": "2020-12-15T16:09:51+0100",
  "props": {},
  "serv": "battery",
  "tags": [],
  "type": "evt.lvl.report",
  "val": 9,
  "val_t": "int"
}

MOTION_MSG = {
  "ctime": "2020-03-26T16:54:29+0100",
  "props": {},
  "serv": "sensor_presence",
  "tags": [],
  "type": "evt.presence.report",
  "val": True,
  "val_t": "bool"
}

OPENED_MSG = {
  "ctime": "2020-03-26T16:54:29+0100",
  "props": {},
  "serv": "sensor_contact",
  "tags": [],
  "type": "evt.open.report",
  "val": True,
  "val_t": "bool"
}

WATER_LEAK_MSG = {
  "ctime": "2020-07-01T13:40:29+0200",
  "props": {},
  "serv": "alarm_water",
  "tags": [],
  "type": "evt.alarm.report",
  "val": {
    "event": "leak",
    "status": "activ"
  },
  "val_t": "str_map"
}

LOCK_DOOR_MSG = {
  "ctime": "2020-12-04T20:19:25+0100",
  "props": {
    "timeout_s": "254",
    "unsecured_desc": ""
  },
  "serv": "door_lock",
  "tags": [],
  "type": "evt.lock.report",
  "val": {
    "bolt_is_locked": False,
    "door_is_closed": False,
    "is_secured": True,
    "latch_is_closed": False
  },
  "val_t": "bool_map"
}



def configure_client(client):
    client.on_message = None
    print("connecting to broker")
    client.connect(MQTT_HOST)


def test_firealarm_notification(client):
    ret = client.publish(FIREALARM_TOPIC, str(SDCO_FIREALARM_MSG).replace("'","\""))
    print('Waiting 10 sec... RETVAL FIREALARM:' + str(ret))
    time.sleep(10)
    deaktiv_msg = SDCO_FIREALARM_MSG
    deaktiv_msg['val']['status'] = 'deactiv'
    ret = client.publish(FIREALARM_TOPIC, str(deaktiv_msg).replace("'", "\""))
    print('Waiting 10 sec... RETVAL FIREALARM DEACTIV:' + str(ret))


def test_temp_level_notificaions(client):
    temp_msg = SDCO_TEMP_MSG
    temp_msg['val'] = 4
    ret = client.publish(TEMPERATURE_TOPIC, str(temp_msg).replace("'", "\""))
    print('Waiting 30 sec... RETVAL battery:' + str(ret))
    time.sleep(30)
    temp_msg['val'] = -1
    ret = client.publish(TEMPERATURE_TOPIC, str(temp_msg).replace("'", "\""))
    print('Waiting 30 sec... RETVAL battery:' + str(ret))
    time.sleep(30)
    temp_msg['val'] = 19
    ret = client.publish(TEMPERATURE_TOPIC, str(temp_msg).replace("'", "\""))
    time.sleep(10)
    temp_msg['val'] = 46
    ret = client.publish(TEMPERATURE_TOPIC, str(temp_msg).replace("'", "\""))
    print('Waiting 30 sec... RETVAL battery:' + str(ret))
    time.sleep(30)
    temp_msg['val'] = 56
    ret = client.publish(TEMPERATURE_TOPIC, str(temp_msg).replace("'", "\""))
    print('Waiting 30 sec... RETVAL battery:' + str(ret))
    time.sleep(30)


def test_tampering_notification(client):
    tampering_msg = TAMPERING_MSG
    ret = client.publish(TAMPERING_TOPIC, str(tampering_msg).replace("'", "\""))
    print('Waiting 20 sec... RETVAL tampering:' + str(ret))
    time.sleep(20)
    tampering_msg['val']['status'] = 'deactiv'
    ret = client.publish(TAMPERING_TOPIC, str(tampering_msg).replace("'", "\""))
    print('Waiting 20 sec... RETVAL tampering deactiv:' + str(ret))
    time.sleep(20)


def test_battery_level_notification(client):
    battery_msg = SDCO_BATTERY_MSG
    ret = client.publish(BATTERY_TOPIC, str(battery_msg).replace("'", "\""))
    print('Waiting 20 sec... Battery low retval:' + str(ret))
    time.sleep(20)
    battery_msg['val'] = 51
    ret = client.publish(BATTERY_TOPIC, str(battery_msg).replace("'", "\""))
    print('Waiting 20 sec... Battery low retval:' + str(ret))
    time.sleep(20)


def test_motion_away_notification(client):
    motion_msg = MOTION_MSG
    ret = client.publish(MOTION_TOPIC, str(motion_msg).replace("'", "\""))
    print('Waiting 20 sec... Motion (in away mode) retval:' + str(ret))
    time.sleep(20)


def test_opened_away_notification(client):
    opened_msg = OPENED_MSG
    ret = client.publish(OPENED_TOPIC, str(opened_msg).replace("'", "\""))
    print('Waiting 20 sec... Contactron (in away mode) retval:' + str(ret))
    time.sleep(20)


def test_waterleak_notification(client):
    leak_msg = WATER_LEAK_MSG
    ret = client.publish(WATERLEAK_TOPIC, str(leak_msg).replace("'", "\""))
    print('Waiting 20 sec... Water leak retval:' + str(ret))
    time.sleep(20)
    leak_msg['val']['status'] = 'deactiv'
    ret = client.publish(WATERLEAK_TOPIC, str(leak_msg).replace("'", "\""))
    print('Waiting 20 sec... Water leak retval:' + str(ret))


client = mqtt.Client("Notfication_mock_1")
configure_client(client)
print("Client confrigured. Starting the loop. ALARM TOPIC:" + FIREALARM_TOPIC)
client.loop_start()

test_firealarm_notification(client)
test_temp_level_notificaions(client)
test_tampering_notification(client)
test_battery_level_notification(client)

test_motion_away_notification(client)
test_opened_away_notification(client)

client.loop_stop()
