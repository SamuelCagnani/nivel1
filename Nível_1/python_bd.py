import paho.mqtt.client as mqtt
import json
import mysql.connector
from mysql.connector import Error

# Configurações MQTT
mqtt_server = "e6e2fd9238274ac7b5cd5c8d3f037020.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_user = "hivemq.webclient.1732642709438"
mqtt_password = "GFl5Y2Hs?Xh3iE:$1;dy"

# Tópico que será assinado
topic = "sensores/dados"

# Configurações do Banco de Dados
db_config = {
    "host": "localhost",  # Altere para o IP do servidor MySQL, se não for local
    "user": "ana",  # Substitua pelo usuário do MySQL
    "password": "1234",  # Substitua pela senha do MySQL
    "database": "workbench"
}

# Função para inserir dados no banco de dados
def salvar_dados(temperatura, umidade, qualidade_ar):
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """
                INSERT INTO sensor (temperatura, umidade, qualidade_ar)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (temperatura, umidade, qualidade_ar))
            connection.commit()
            print("Dados salvos no banco com sucesso!")
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Função chamada quando a conexão é bem-sucedida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
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

        # Extrai os valores do JSON
        temperatura = data['temperatura']
        umidade = data['umidade']
        qualidade_ar = data['qualidade_ar']

        print("Mensagem recebida (JSON):")
        print(f"Temperatura: {temperatura}°C")
        print(f"Umidade: {umidade}%")
        print(f"Qualidade do ar: {qualidade_ar}")

        # Salva os dados no banco
        salvar_dados(temperatura, umidade, qualidade_ar)

    except json.JSONDecodeError:
        print("Erro: Mensagem recebida não está em formato JSON válido!")
    except KeyError as e:
        print(f"Erro: Chave JSON ausente: {e}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
print("Conectando ao broker...")
client.connect(mqtt_server, mqtt_port, 60)

# Loop para manter o cliente funcionando
client.loop_forever()
