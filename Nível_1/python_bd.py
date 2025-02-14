import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from datetime import datetime
import logging
from passwords import keys

mqtt_server = keys['MQTT_SERVER']
mqtt_port = 8883
mqtt_user = keys['MQTT_USER']
mqtt_password = keys['MQTT_PASSWORD']

topics = ["sensores/temperatura", "sensores/umidade", "sensores/qualidade_do_ar"]

uri = keys['BD_oficial_key']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def conectarMongoDB():
    global client_mongo, collection
    try:
        client_mongo = MongoClient(uri)
        client_mongo.admin.command("ping")
        logger.info("Conexão bem-sucedida com o MongoDB!")
        db = client_mongo['Extensao']
        collection = db['sensores']
    except ConnectionFailure as e:
        logger.error("Erro ao conectar ao MongoDB")
        exit(1)

def salvar_dados(temperatura, umidade, qualidade_ar):
    try:
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conjunto_dados = {
            "data_hora": data_hora_atual,
            "temperatura": temperatura,
            "umidade": umidade,
            "qualidade_ar": qualidade_ar
        }
        collection.insert_one(conjunto_dados)
        logger.info("Dados salvos com sucesso!")
    except PyMongoError as e:
        logger.error(f"Erro ao salvar no MongoDB: {e}")

dados_recebidos = {
    "temperatura": None,
    "umidade": None,
    "qualidade_ar": None
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
        for topic in topics:
            client.subscribe(topic)
        print(f"Assinado nos tópicos: {topics}")
    else:
        print(f"Erro ao conectar. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    global dados_recebidos
    try:
        valor = float(msg.payload.decode()) 

        if msg.topic == "sensores/temperatura":
            dados_recebidos["temperatura"] = valor
        elif msg.topic == "sensores/umidade":
            dados_recebidos["umidade"] = valor
        elif msg.topic == "sensores/qualidade_do_ar":
            dados_recebidos["qualidade_ar"] = valor

        print(f"Recebido -> {msg.topic}: {valor}")

        if all(v is not None for v in dados_recebidos.values()):
            salvar_dados(dados_recebidos["temperatura"], dados_recebidos["umidade"], dados_recebidos["qualidade_ar"])
            dados_recebidos = {"temperatura": None, "umidade": None, "qualidade_ar": None}  # Reseta os valores

    except ValueError:
        print(f"Erro ao converter valor recebido de {msg.topic}")

conectarMongoDB()
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message

print("Conectando ao broker...")
client.connect(mqtt_server, mqtt_port, 60)
#
client.loop_forever()
