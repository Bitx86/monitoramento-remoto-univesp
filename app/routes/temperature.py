from flask import Blueprint, request, jsonify
from app.config import DB_CONFIG
import psycopg2

temperature_bp = Blueprint("temperature", __name__)

@temperature_bp.route("/temperature", methods=["POST"])
def log_temperature():
    data = request.get_json()
    device_id = data.get("device_id")
    api_key = data.get("api_key")
    temperature = data.get("temperature")

    # Validar device e api_key
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id FROM devices WHERE id=%s AND api_key=%s", (device_id, api_key))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "Dispositivo inválido"}), 401

    # Inserir log
    cur.execute("""
        INSERT INTO temperature_logs (device_id, temperature)
        VALUES (%s, %s)
    """, (device_id, temperature))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Temperatura registrada"})
