from azure.iot.device import IoTHubDeviceClient, Message  

CONNECTION_STRING = "HostName=hub-anthanh.azure-devices.net;DeviceId=node;SharedAccessKey=wkA5fp+tmLyjmO1AmK+jefmZKUhYMxekjGOAJmLEXWY=" 
MSG_SND = '{{"temperature": {temperature},"humidity": {humidity}}}' 

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING) 

def send_azure(jsonData)
    data = json.loads(jsonData)
    humidity = data['humidity']
    temperature = data['temperature']
    msg_txt_formatted = MSG_SND.format(temperature=temperature, humidity=humidity)
    message = Message(msg_txt_formatted)
    print( "Sending message: {}".format(message) )
    client.send_message(message)
    print ( "Message successfully sent" )   