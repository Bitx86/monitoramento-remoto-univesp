import ssl
import json
import os
import paho.mqtt.client as mqtt
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv("../.env", override=True)

# Credenciais admin MQTT
admin = {
    "username": "admin",
    "password": os.getenv("MOSQUITTO_ADMIN_PASS"),
    "broker": os.getenv("HOSTNAME"),
    "port": 8883
}

# Configuração do PostgreSQL
db_config = {
    "host": "localhost",
    "port": 5432,
    "dbname": os.getenv("DB_DB"),
    "user":  os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

# Conecta ao PostgreSQL
conn = psycopg2.connect(**db_config)
conn.autocommit = True
cursor = conn.cursor()

# Callback MQTT: conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso como admin!")
        client.subscribe("users/+/devices/+/#")  # ouve todos os devices
    else:
        print("Falha na conexão, código:", rc)

# Callback MQTT: mensagem recebida
def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        print(f"Tópico: {msg.topic}")
        print(f"Mensagem: {payload_str}")
        print("------")

        # Decodifica JSON
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            payload = {}

        # Extrai device_id do tópico MQTT
        # Tópico: users/<user_id>/devices/<device_id>/...
        device_id_text = msg.topic.split("/")[3]

        # Busca UUID interno na tabela devices
        cursor.execute("SELECT id FROM devices WHERE device_id = %s AND is_active = true", (device_id_text,))
        row = cursor.fetchone()
        if not row:
            print(f"Dispositivo não encontrado ou inativo: {device_id_text}")
            return

        device_uuid = row[0]

        # Extrai temperature e humidity do payload se existirem
        temperature = payload.get("temperatura")
        humidity = payload.get("humidity")

        # Converte para float, arredondando 2 casas decimais
        if temperature is not None:
            temperature = round(float(temperature), 2)
        if humidity is not None:
            humidity = round(float(humidity), 2)
        print(temperature, humidity)
        # Insere no PostgreSQL
        cursor.execute("""
            INSERT INTO device_telemetry (device_id, temperature, humidity, payload)
            VALUES (%s, %s, %s, %s::jsonb)
        """, (device_uuid, temperature, humidity, json.dumps(payload)))

    except Exception as e:
        print("Erro ao gravar no banco:", e)

# Cria cliente MQTT
client = mqtt.Client(client_id="admin_listener")
client.username_pw_set(username=admin['username'], password=admin['password'])
client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

client.connect(admin['broker'], admin['port'])
client.loop_forever()