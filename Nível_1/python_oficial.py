import paho.mqtt.client as mqtt

# Configurações MQTT
mqtt_server = "e6e2fd9238274ac7b5cd5c8d3f037020.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_user = "hivemq.webclient.1732642709438"
mqtt_password = "GFl5Y2Hs?Xh3iE:$1;dy"

# Tópicos a serem assinados
topics = [
    ("sensores/temperatura", 0),
    ("sensores/umidade", 0),
    ("sensores/qualidade_do_ar", 0),
]

# Função chamada quando a conexão é bem-sucedida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
        # Assinar os tópicos
        for topic, qos in topics:
            client.subscribe(topic)
            print(f"Assinado no tópico: {topic}")
    else:
        print(f"Erro ao conectar. Código de retorno: {rc}")

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print(f"Tópico: {msg.topic} | Mensagem: {msg.payload.decode()}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.tls_set()  # Configura TLS para conexões seguras
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
print("Conectando ao broker...")
client.connect(mqtt_server, mqtt_port, 60)

# Loop para manter o cliente funcionando
client.loop_forever()
