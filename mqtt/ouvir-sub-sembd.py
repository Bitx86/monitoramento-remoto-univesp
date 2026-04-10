import ssl
import json
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv("../.env", override=True)

admin = {
    "username": "admin",
    "password": os.getenv("MOSQUITTO_ADMIN_PASS"),
    "broker": os.getenv("HOSTNAME"),
    "port": 8883
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso como admin!")
        client.subscribe("users/+/devices/+/#")
    else:
        print("Falha na conexão, código:", rc)

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        print(f"Tópico: {msg.topic}")
        print(f"Mensagem: {payload_str}")
        print("------")
    except Exception as e:
        print("Erro ao processar mensagem:", e)

client = mqtt.Client(client_id="admin_listener")
client.username_pw_set(username=admin['username'], password=admin['password'])
client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

client.connect(admin['broker'], admin['port'])
client.loop_forever()