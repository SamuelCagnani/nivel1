import paho.mqtt.client as mqtt
import json  # Para manipular JSON

# Configurações MQTT
mqtt_server = "e6e2fd9238274ac7b5cd5c8d3f037020.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_user = "hivemq.webclient.1732642709438"
mqtt_password = "GFl5Y2Hs?Xh3iE:$1;dy"

# Tópico que será assinado
topic = "sensores/dados"

# Função chamada quando a conexão é bem-sucedida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
        # Assinar o tópico de dados JSON
        client.subscribe(topic)
        print(f"Assinado no tópico: {topic}")
    else:
        print(f"Erro ao conectar. Código de retorno: {rc}")

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    try:
        # Decodifica a mensagem e carrega como JSON
        payload = msg.payload.decode()
        data = json.loads(payload)
        
        # Exibe os valores extraídos do JSON
        print("Mensagem recebida (JSON):")
        print(f"Temperatura: {data['temperatura']}°C")
        print(f"Umidade: {data['umidade']}%")
        print(f"Qualidade do ar: {data['qualidade_ar']}")
    except json.JSONDecodeError:
        print("Erro: Mensagem recebida não está em formato JSON válido!")
    except KeyError as e:
        print(f"Erro: Chave JSON ausente: {e}")

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
