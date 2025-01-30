import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient             # pip install pymongo
from pymongo.errors import ConnectionFailure, PyMongoError
from datetime import datetime
import logging
from passwords import keys     # Arquivo para colocar todos os links e passwords

# Configurações MQTT
mqtt_server = keys['MQTT_SERVER']
mqtt_port = 8883
mqtt_user = keys['MQTT_USER']
mqtt_password = keys['MQTT_PASSWORD']

# Tópico que será assinado
topic = "sensores/dados"

# Mongo Uri
uri = keys['MONGO_URI']

# Configurações do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def conectarMongoDB():
    global client_mongo, collection
    try:
        client_mongo = MongoClient(uri)
        client_mongo.admin.command("ping")
        logger.info("Conexão estabelecida bem sucedida com o MongoDB!")
        db = client_mongo['sensor_data']
        collection = db['leituras']
    except ConnectionFailure as e:
        logger.error(f"Erro ao conectar ao MongoDB")
        exit(1)
    

# Função para inserir dados no banco de dados
def salvar_dados(temperatura, umidade, qualidade_ar):
    try:
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conjunto_dados = {
            "data_hora" : data_hora_atual,
            "umidade" : umidade,
            "temperatura" : temperatura,
            "qualidade_ar" : qualidade_ar
        }
        
        collection.insert_one(conjunto_dados)
        logger.info("Dados salvos com sucesso!")
    except PyMongoError as e:
        logger.error(f"Erro ao conectar ao MongoDB: {e}")
        

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


client_mongo = None
collection = None
conectarMongoDB()

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
