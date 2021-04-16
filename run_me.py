import paho.mqtt.client as mqtt
import json
import random
from time import sleep
from azure.iot.device import IoTHubDeviceClient, Message  
import pymysql
from datetime import datetime
#from save_database import save

# Azure server
CONNECTION_STRING = "HostName=hub-anthanh.azure-devices.net;DeviceId=node;SharedAccessKey=wkA5fp+tmLyjmO1AmK+jefmZKUhYMxekjGOAJmLEXWY=" 
MSG_SND = '{{"temperature": {temperature},"humidity": {humidity}}}' 

azure = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING) 

# Mosquiito Broker setting
MQTT_Broker = "192.168.137.196"
MQTT_Port = 1883
Keep_Alive_Interval = 7200
MQTT_Topic = 'hello'

def send_azure(jsonData):
    data = json.loads(jsonData)
    humidity = data['humidity']
    temperature = data['temperature']
    msg_txt_formatted = MSG_SND.format(temperature=temperature, humidity=humidity)
    message = Message(msg_txt_formatted)
    print( "Sending azure: {}".format(message) )
    azure.send_message(message)
    print ( "Message successfully sent" )   

def save(data):    
	json_Dict = json.loads(data)
	#print(data)
	Temperature = json_Dict['temperature']
	Humidity = json_Dict['humidity']
	Time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

	db = pymysql.connect("localhost", "root", "admin999999999", "azure")
	cursor = db.cursor()
	# Execute
	cursor.execute("INSERT INTO Xuanthuy(Temperature, Humidity, Time) VALUES(%s,%s,%s)",(Temperature,Humidity,Time))
	print(">> save database azure - table Xuanthuy!")
	db.commit()
	db.close()

# Callback server
def on_connect(client, userdata, flags, rc):
    if rc != 0:
        pass
    else:
        print("Connection returned result: " + str(MQTT_Broker))
    client.subscribe(MQTT_Topic, qos = 1)

# Callback on_message server
def on_message(client, userdata, msg):
    print("Message Broker  Recieved: "+msg.payload.decode())
    send_azure(msg.payload)
    save(msg.payload) #save database
    #mosquitto_pub -d -t hello -m "{\"Area\":\"xuanthuy\",\"ID\":1,\"Temperature\":4,\"Humidity\":45}"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_Broker, MQTT_Port, Keep_Alive_Interval)
client.loop_forever()
