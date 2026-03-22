import secrets
import string
import bcrypt
from flask import Blueprint, request, jsonify, g
from app.repositories.device_repository import create_device, get_devices_by_user
from app.utils.auth_utils import decode_jwt
from app.repositories.mosquitto_repository import configure_mosquitto

devices_bp = Blueprint("devices", __name__)

def generate_device_id():
    return "dkey-" + secrets.token_hex(4)

def generate_secret(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@devices_bp.route('/api/devices', methods=['POST'])
def add_device():
    if g.user['role'] != 'tecnicos' and g.user['role'] != 'admin':
        return jsonify({"error": "unauthorized"}), 403

    data = request.get_json()
    name = data.get('name')
    if len(name) < 5:
        return jsonify({"error": "Nome do dispositivo dever ter mais de 5 caracteres."}), 403
  
    device_id = generate_device_id()
    secret = generate_secret()

    secret_hash = bcrypt.hashpw(secret.encode(), bcrypt.gensalt()).decode()
    create_device(g.user['user_id'], device_id, name, secret_hash)
    
    configure_mosquitto(device_id,secret,g.user['user_id'])
    cert = ""
    crtfile = open("/etc/mosquitto/certs/ca.crt","r")
    cert = crtfile.read()
    return jsonify({
        "device_id": device_id,
        "secret": secret,
        "broker": "mqtts://35.209.244.156:8883",
        "port": 8883,
        "topic": f"users/{g.user['user_id']}/devices/{device_id}/",
        "cert": cert
    })

@devices_bp.route("/devices", methods=["GET"])
def list_devices():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_data = decode_jwt(token)
    user_id = user_data["user_id"]

    devices = get_devices_by_user(user_id)
    return jsonify(devices)
