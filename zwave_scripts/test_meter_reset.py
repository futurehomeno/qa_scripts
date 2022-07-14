from time import sleep
from datetime import datetime

import paho.mqtt.client as mqtt
import json

DEVICES_ADDR_LIST = []

MQTT_HOST = 'localhost'
METER_ELEC_TOPIC_WRITE = "pt:j1/mt:cmd/rt:dev/rn:zw/ad:1/sv:meter_elec/ad:{}"
METER_ELEC_TOPIC_GET = "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:meter_elec/ad:{}"

RESET_METER_MSG = {
  "serv": "meter_elec",
  "type": "cmd.meter.reset",
  "val_t": "null",
  "val": None,
  "props": {},
  "tags": None,
  "src": "-",
  "ver": "1",
  "uid": "932c9611-9386-4ac4-bda2-38d56e9f88b9",
  "topic": "pt:j1/mt:cmd/rt:dev/rn:zw/ad:1/sv:meter_elec/ad:124_0"
}

METER_ELEC_GET_REPORT_MSG = {
  "serv": "meter_elec",
  "type": "cmd.meter.get_report",
  "val_t": "string",
  "val": "",
  "props": None,
  "tags": None,
  "corid": "",
  "ctime": "",
  "src": "tplex-ui",
  "ver": "1",
  "uid": "46dd96a2-9388-451c-b3f6-e43cfa4cb228",
  "topic": "pt:j1/mt:cmd/rt:dev/rn:zw/ad:1/sv:meter_elec/ad:124_0"
}


class MeterResetTester:

    def __init__(self):
        print("Starting mrt constructor")
        self.current_energy_measured = None
        client = mqtt.Client("test_reset")
        client.on_message = self.on_message
        print("connecting to broker")
        client.connect(MQTT_HOST)
        client.loop_start()
        self.client = client

    def on_message(self, client, userdata, message):
        msg_str = str(message.payload.decode("utf-8"))
        print("message received " + msg_str)
        print("message topic=", message.topic)
        print("Measured energy:" + str(json.loads(msg_str)['val']))
        self.current_energy_measured = float(str(json.loads(msg_str)['val']))

    def check_dev_energy_meter(self, addr):
        new_msg = METER_ELEC_GET_REPORT_MSG
        new_msg['topic'] = addr
        import uuid
        uid_new = str(uuid.uuid1())
        print("New uid:" + str(uid_new))
        new_msg['uid'] = uid_new
        date = datetime.now()
        print("Adding ctime: " + str(date))
        new_msg['ctime'] = str(date.isoformat())
        msg_parsed = str(new_msg).replace("'", "\"")
        ret = self.client.publish(addr, msg_parsed)
        print('RETVAL:' + str(ret))
        sleep(4)

    def send_device_reset_meter(self, addr):
        new_msg = RESET_METER_MSG
        new_msg['topic'] = addr
        msg_parsed = str(new_msg).replace("'", "\"")
        ret = self.client.publish(addr, msg_parsed)
        print('RETVAL:' + str(ret))
        sleep(4)

    def test_reset_measurement(self, addr):
        self.client.subscribe(METER_ELEC_TOPIC_GET.format('124_0'))
        self.check_dev_energy_meter(addr)
        measurement_before = self.current_energy_measured
        assert measurement_before != 0, "Nothing to reset if device meter elec reports 0 kWh"
        self.send_device_reset_meter(addr)
        sleep(10)
        self.check_dev_energy_meter(addr)
        measurement_after_reset = self.current_energy_measured
        assert measurement_after_reset == 0, "Device is reporting non-zero ({}) " \
                                             "energy measurement after the reset!".format(measurement_after_reset)


print("Launching the test procedure...")
mrt = MeterResetTester()
addr = METER_ELEC_TOPIC_WRITE.format('124_0')
print("ADDR:" + str(addr))
mrt.test_reset_measurement(addr)
mrt.client.loop_stop()

