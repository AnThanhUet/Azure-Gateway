#include <ESP8266WiFi.h>
#include <PubSubClient.h>

//#include <DHT.h>
//#define DHTPIN D7
//#define DHTTYPE DHT11
/*==========================================================*/
const char* ssid = "Ahihi";                
const char* password =  "nguyenthean";           
const char* mqttServer = "192.168.137.196";            
/*==========================================================*/

unsigned long b_time;
String clientId = "ClientESP8266"; 
            
/*==========================================================*/
const char* m_topic = "hello";               
/*==========================================================*/

/*==========================================================*/
WiFiClient espClient;
//DHT dht(DHTPIN, DHTTYPE);
/*==========================================================*/

PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup() {
  Serial.begin(115200);
  //dht.begin();
  setup_wifi();
  /* Hàm start - read Callback client */
  client.setServer(mqttServer, 1883);     
  client.setCallback(callback);
}

/*============= CONNECT WIFI =====================*/
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
/*==========================================================*/

/*=================== CALL BACK =======================================*/
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message read [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  xulidulieu(payload);
}


void xulidulieu(byte* data)
{
  /* Xử lí dữ liệu đọc về tại đây */
}

/*=================== RECONNECT =======================*/
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.publish(m_topic, "Reconnect");               // Gửi dữ liệu
      client.subscribe(m_topic);                          // Theo dõi dữ liệu
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      // Doi 1s
      delay(1000);
    }
  }
}
/*==========================================================*/

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  /* Mỗi 1s gửi dữ liệu thời gian lên topic server*/
  long now = millis();
  if (now - lastMsg > 1000) {
    float h = random(50,70);
    float t = random(20,30);
    String temperature = String(t);
    String humidity = String(h);

    String payload = "{";
//    payload += "\"Area\":"; payload += "XuanThuy"; payload += ",";
//    payload += "\"ID\":"; payload += "1"; payload += ",";

    payload += "\"temperature\":"; payload += temperature; payload += ",";
    payload += "\"humidity\":"; payload += humidity;
    payload += "}";

    char telemetry[100];
    payload.toCharArray( telemetry, 100 );
    client.publish(m_topic, telemetry );
    Serial.println( telemetry);
    lastMsg = now;
  }
}
