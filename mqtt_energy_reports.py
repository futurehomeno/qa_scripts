import paho.mqtt.client as mqtt
import time

MQTT_HOST = 'localhost'
ENERGY_TOPIC = 'pt:j1/mt:cmd/rt:app/rn:ecollector/ad:1'
PUBLISH_TOPIC = 'pt:j1/mt:rsp/rt:cloud/rn:remote-client/ad:smarthome-app'

RESPONSE = {
  "serv": "ecollector",
  "type": "evt.tsdb.data_points_report",
  "val_t": "object",
  "val": {
    "Results": [
      {
        "Series": [
          {
            "name": "electricity_meter_energy_sampled",
            "tags": {
              "dev_type": "light."
            },
            "columns": [
              "time",
              "value"
            ],
            "values": [
              [
                1627336800,
                None
              ],
              [
                1627340400,
                120.9999980926514005
              ],
              [
                1627344000,
                1230.0000001192093007
              ],
              [
                1627347600,
                0.020000010728836004
              ],
              [
                1627351200,
                0.01999998092651295
              ],
              [
                1627354800,
                0.020000010728836004
              ],
              [
                1627358400,
                0.030000001192093007
              ],
              [
                1627362000,
                0.020000010728836004
              ],
              [
                1627365600,
                0.019999980926514005
              ],
              [
                1627369200,
                0.020000010728836004
              ],
              [
                1627372800,
                0.019999980926514005
              ],
              [
                1627376400,
                0.020000040531158003
              ],
              [
                1627380000,
                0.019999980926514005
              ],
              [
                1627383600,
                0.019999980926513006
              ],
              [
                1627387200,
                0.020000040531159002
              ],
              [
                1627390800,
                None
              ],
              [
                1627394400,
                None
              ],
              [
                1627398000,
                None
              ],
              [
                1627401600,
                None
              ],
              [
                1627405200,
                None
              ],
              [
                1627408800,
                None
              ],
              [
                1627412400,
                None
              ],
              [
                1627416000,
                None
              ],
              [
                1627419600,
                None
              ],
              [
                1627423200,
                None
              ]
            ]
          }
        ],
        "Messages": None
      }
    ]
  },
  "props": None,
  "tags": None,
  "src": "-",
  "ver": "1",
  "uid": "3e6449db-57db-43eb-8333-7791c28b287a",
  "topic": "pt:j1/mt:rsp/rt:cloud/rn:remote-client/ad:smarthome-app"
}


def configure_client(client):
    client.on_message = on_message
    print("connecting to broker")
    client.connect(MQTT_HOST)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    if message.topic == ENERGY_TOPIC:
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
print("Subscribing to app version topic:", ENERGY_TOPIC)
client.subscribe(ENERGY_TOPIC)
time.sleep(60)
client.loop_stop()
