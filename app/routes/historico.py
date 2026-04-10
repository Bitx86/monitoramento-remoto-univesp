from flask import Blueprint, jsonify, g
from psycopg2.extras import RealDictCursor
from app.repositories.db_repository import get_db_connection
import logging
from flask import current_app

historico_bp = Blueprint('historico', __name__)

@historico_bp.route("/api/dados-grafico")
def get_dados():
    if not g.user:
        return jsonify({"erro": "não autenticado"}), 401

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:

                # devices do usuário
                cur.execute("""
                    SELECT id, device_id, name
                    FROM devices
                    WHERE user_id = %s
                """, (g.user['user_id'],))
                devices = cur.fetchall()

                current_app.logger.info(f"Resultado devices get_dados(): {devices}")

                if not devices:
                    current_app.logger.error(f"Dispositivos não achados {g.user['user_id']}")
                    return jsonify({"devices": {}})

                device_ids = [d['id'] for d in devices]

                # pega últimos registros por device (window function)
                cur.execute("""
                    SELECT *
                    FROM (
                        SELECT 
                            device_id,
                            temperature,
                            created_at,
                            ROW_NUMBER() OVER (
                                PARTITION BY device_id 
                                ORDER BY created_at DESC
                            ) as rn
                        FROM device_telemetry
                        WHERE device_id = ANY(%s::uuid[])
                    ) t
                    WHERE rn <= 30
                    ORDER BY device_id, created_at ASC
                """, (device_ids,))

                rows = cur.fetchall()

                current_app.logger.info(f"Resultado get_dados(): {rows}")

                # organiza por device
                resultado = {}

                # map para nome amigável
                device_map = {
                    d['id']: {
                        "device_id": d['device_id'],
                        "name": d['name']
                    } for d in devices
                }

                for row in rows:
                    did = row['device_id']

                    if did not in resultado:
                        resultado[did] = {
                            "info": device_map.get(did, {}),
                            "valores": [],
                            "timestamps": []
                        }

                    if row['temperature'] is not None:
                        resultado[did]["valores"].append(float(row['temperature']))
                        resultado[did]["timestamps"].append(row['created_at'].isoformat())

                return jsonify({"devices": resultado})

    except Exception:
        current_app.logger.exception("Erro ao buscar dados do gráfico")
        return jsonify({"erro": "erro interno"}), 500