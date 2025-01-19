#include <DHT.h>

// Configurações do sensor DHT11
#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Configurações do sensor MQ-135
#define MQ135_PIN A0 // Pino analógico para o MQ-135

void setup()
{
  Serial.begin(115200);
  Serial.println("Inicializando sensores...");

  dht.begin();
  Serial.println("Sensores inicializados!");
}

void loop()
{
  // Leitura do DHT11
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();

  // Leitura do MQ-135
  int mq135Value = analogRead(MQ135_PIN);

  // Verificação de erro na leitura do DHT11
  if (isnan(temperatura) || isnan(umidade))
  {
    Serial.println("Erro ao ler do sensor DHT11!");
    return;
  }

  // Exibe os dados no terminal serial
  Serial.println("Leituras dos sensores:");
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" °C");

  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println(" %");

  Serial.print("Qualidade do ar (MQ-135): ");
  Serial.println(mq135Value);

  Serial.println("-----------------------------");

  delay(2000); // Aguarda 2 segundos antes da próxima leitura
}