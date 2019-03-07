#Python imports
import random



# Custom pip imports
import paho.mqtt.client as mqtt # https://pypi.org/project/paho-mqtt/



# Application imports
import secrets



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # Reconnect then subscriptions will be renewed.
    client.subscribe([(userdata[0], 0)])
    client.publish(userdata[0], userdata[1], 0, True)

# Called when a message has been received on a topic that the client subscribes to .
def on_message(client, userdata, msg):
    # print("Message received:", msg.topic+" "+str(msg.payload, 'utf-8'))
    if str(msg.topic) == str(userdata[0]) and str(msg.payload, 'utf-8') == str(userdata[1]):
        # print("Received correct message!")
        client.disconnect()

def send_notification():
    # print("Send Notification")
    # If multiple Topics, notify a random one
    if len(secrets.clientTopics) > 1:
        topicInd = random.randint(0, len(secrets.clientTopics) - 1)
    else:
        topicInd = 0
    try:
        client = mqtt.Client('weekly-random-reminder', False)
        client.username_pw_set(secrets.clientUserName, secrets.clientPass)
        client.user_data_set([secrets.clientTopics[topicInd], secrets.clientPayload])
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(secrets.clientIP, secrets.clientPort)
        client.loop_forever()
    except ConnectionRefusedError as e:
        errors.append(str(today)+":\tConnection refused. Is the MQTT broker online?")
