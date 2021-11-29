import paho.mqtt.client as mqtt
import time

MQTT_HOST = 'localhost'
VERSION_TOPIC = 'pt:j1/mt:cmd/rt:app/rn:fhbutler/ad:1'
PUBLISH_TOPIC = 'pt:j1/mt:rsp/rt:cloud/rn:remote-client/ad:smarthome-app'

RESPONSE = {
  "serv": "fhbutler",
  "type": "evt.app.version_report",
  "val_t": "object",
  "val": [
    {
      "name": "futurehome-security",
      "status": "install ok installed",
      "ver": "1.0.0",
      "update_ver": ""
    },
    {
      "name": "vinculum",
      "status": "install ok installed",
      "ver": " ",
      "update_ver": ""
    },
    {
      "name": "fhbutler",
      "status": "install ok installed",
      "ver": "",
      "update_ver": ""
    },
    {
      "name": "fh-drop",
      "status": "install ok installed",
      "ver": "1.0.1",
      "update_ver": ""
    },
    {
      "name": "nanoprobe",
      "status": "install ok installed",
      "ver": "1.1.4+fimp",
      "update_ver": "1.1.4+fimp-beta"
    },
    {
      "name": "fh-selftest",
      "status": "install ok installed",
      "ver": "1.0.10",
      "update_ver": ""
    },
    {
      "name": "angrydog",
      "status": "install ok installed",
      "ver": "1.0.13",
      "update_ver": ""
    },
    {
      "name": "fh-watchdog-conf",
      "status": "install ok installed",
      "ver": "0.9.1",
      "update_ver": ""
    },
    {
      "name": "zigbee-ad",
      "status": "install ok installed",
      "ver": "0.3.14ATetts",
      "update_ver": ""
    },
    {
      "name": "zigbee-selftest",
      "status": "install ok installed",
      "ver": "1.1.2",
      "update_ver": ""
    },
    {
      "name": "fh-iptables-rules",
      "status": "install ok installed",
      "ver": "1.0.0~beta1",
      "update_ver": ""
    },
    {
      "name": "fh-switch-archive",
      "status": "install ok installed",
      "ver": "1.0.0",
      "update_ver": ""
    },
    {
      "name": "factory-tool",
      "status": "install ok installed",
      "ver": "1.0.2",
      "update_ver": ""
    },
    {
      "name": "zwave-ad",
      "status": "install ok installed",
      "ver": "1.0.7144",
      "update_ver": ""
    },
    {
      "name": "futurehome-common",
      "status": "install ok installed",
      "ver": "1.0",
      "update_ver": ""
    },
    {
      "name": "fh-hardware",
      "status": "install ok installed",
      "ver": "1.0.6",
      "update_ver": ""
    },
    {
      "name": "fh-emergency-channel",
      "status": "install ok installed",
      "ver": "1.0.3",
      "update_ver": ""
    },
    {
      "name": "escapepod",
      "status": "install ok installed",
      "ver": "1.0",
      "update_ver": "1.0.1~beta"
    },
    {
      "name": "influxdb",
      "status": "install ok installed",
      "ver": "1.7.3-1+noreport",
      "update_ver": ""
    },
    {
      "name": "kind-owl",
      "status": "install ok installed",
      "ver": "1.3.3",
      "update_ver": ""
    },
    {
      "name": "fimp-upgrade",
      "status": "install ok installed",
      "ver": "1.0.4",
      "update_ver": ""
    },
    {
      "name": "tpflow",
      "status": "install ok installed",
      "ver": "1.0.2",
      "update_ver": ""
    },
    {
      "name": "red-bee",
      "status": "install ok installed",
      "ver": "1.1.0",
      "update_ver": "2.0.1"
    },
    {
      "name": "futurehome",
      "status": "install ok installed",
      "ver": "2.0.4",
      "update_ver": ""
    },
    {
      "name": "futurehome-core",
      "status": "install ok installed",
      "ver": "1.2.1",
      "update_ver": ""
    },
    {
      "name": "zipgateway",
      "status": "install ok installed",
      "ver": "7.14.103",
      "update_ver": ""
    },
    {
      "name": "fh-installsigned",
      "status": "install ok installed",
      "ver": "1.0.1",
      "update_ver": ""
    },
    {
      "name": "mosquitto",
      "status": "install ok installed",
      "ver": "1.6.2-0mosquitto1~jessie1",
      "update_ver": ""
    },
    {
      "name": "fh-zw-flash",
      "status": "install ok installed",
      "ver": "1.0.0",
      "update_ver": ""
    },
    {
      "name": "fimpui",
      "status": "install ok installed",
      "ver": "1.1.9",
      "update_ver": ""
    },
    {
      "name": "cloud-bridge",
      "status": "install ok installed",
      "ver": "1.3.8",
      "update_ver": "1.4.1"
    },
    {
      "name": "backup-restore",
      "status": "install ok installed",
      "ver": "1.5.0",
      "update_ver": ""
    },
    {
      "name": "futurehome-time",
      "status": "install ok installed",
      "ver": "1.0.1",
      "update_ver": ""
    }
  ],
  "props": None,
  "tags": None,
  "src": "-",
  "ver": "1",
  "uid": "61155441-44f0-4195-821b-482ccc6b8f48",
  "corid": "321123",
  "topic": "pt:j1/mt:rsp/rt:cloud/rn:remote-client/ad:smarthome-app"
}


def configure_client(client):
    client.on_message = on_message
    print("connecting to broker")
    client.connect(MQTT_HOST)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    if message.topic == VERSION_TOPIC:
        print("message retain flag=", message.retain)
        new_msg = create_version_message(str(message.payload.decode("utf-8")))
        ret = client.publish(PUBLISH_TOPIC, new_msg)
        print('RETVAL:' + str(ret))


def create_version_message(old_msg_payload):
    uid_ind = old_msg_payload.find("uid")
    uid = old_msg_payload[uid_ind+6:uid_ind+42]
    print("UID old:" + str(uid))
    new_reponse = RESPONSE
    import uuid
    uid_new = str(uuid.uuid1())
    new_reponse['uid'] = uid_new
    new_reponse['corid'] = uid
    print("New reponse:" + str(new_reponse).replace("'", "\""))
    return str(new_reponse).replace("'", "\"")


client = mqtt.Client("Version_mock_1")
configure_client(client)
client.loop_start()
print("Subscribing to app version topic:", VERSION_TOPIC)
client.subscribe(VERSION_TOPIC)
time.sleep(60)
client.loop_stop()
