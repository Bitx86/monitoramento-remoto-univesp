from flask import Blueprint, request, jsonify
from app.repositories.device_repository import create_device, get_devices_by_user
from app.utils.auth_utils import decode_jwt

devices_bp = Blueprint("devices", __name__)

@devices_bp.route("/devices", methods=["POST"])
def add_device():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_data = decode_jwt(token)
    user_id = user_data["user_id"]

    data = request.get_json()
    name = data.get("name")
    device = create_device(user_id, name)
    return jsonify(device)

@devices_bp.route("/devices", methods=["GET"])
def list_devices():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_data = decode_jwt(token)
    user_id = user_data["user_id"]

    devices = get_devices_by_user(user_id)
    return jsonify(devices)
