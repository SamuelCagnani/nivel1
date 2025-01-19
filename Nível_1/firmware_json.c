#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h> 
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// Configurações WiFi
const char* ssid = "Samuel";
const char* password = "password";

// Configurações MQTT (HiveMQ Cloud)
const char* mqtt_server = "e6e2fd9238274ac7b5cd5c8d3f037020.s1.eu.hivemq.cloud"; 
const int mqtt_port = 8883;
const char* mqtt_user = "hivemq.webclient.1732642709438";                
const char* mqtt_password = "GFl5Y2Hs?Xh3iE:$1;dy";

WiFiClientSecure espClient;
PubSubClient client(espClient);

// Configurações dos sensores
#define DHTPIN D2  
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MQ135_PIN A0  // Pino analógico para o MQ-135

void setup() {
  Serial.begin(115200);
  setupWiFi();

  // Configuração do cliente MQTT
  espClient.setInsecure(); // Permite conexão sem certificado (apenas para testes)
  client.setServer(mqtt_server, mqtt_port);
  dht.begin();
}

void setupWiFi() {
  delay(10);
  Serial.println("Conectando ao WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    if (client.connect("ESP8266Client", mqtt_user, mqtt_password)) {
      Serial.println("Conectado!");
    } else {
      Serial.print("Falha, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Leitura do DHT11
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  // Leitura do MQ-135
  int mq135Value = analogRead(MQ135_PIN);

  // Verificação de erro na leitura do DHT11
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Erro ao ler do sensor DHT11!");
    return;
  }

  // Criação do objeto JSON
  StaticJsonDocument<200> doc;
  doc["temperatura"] = temperatura;
  doc["umidade"] = umidade;
  doc["qualidade_ar"] = mq135Value;

  // Serializa o JSON para uma string
  char jsonBuffer[200];
  serializeJson(doc, jsonBuffer);

  // Publica os dados no broker MQTT
  client.publish("sensores/dados", jsonBuffer);

  // Exibe os dados no Serial Monitor
  Serial.println("Dados enviados (JSON):");
  Serial.println(jsonBuffer);

  delay(2000);
}
