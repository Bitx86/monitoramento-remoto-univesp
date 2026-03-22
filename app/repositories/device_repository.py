import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DB_CONFIG

def get_devices_by_user(user_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM devices WHERE user_id=%s", (user_id,))
    devices = cur.fetchone()
    cur.close()
    conn.close()
    return devices

def create_device(user_id, device_id, name, device_secret_hash):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO devices (user_id, device_id, name, device_secret_hash)
        VALUES (%s, %s, %s, %s)
    """, (user_id, device_id, name, device_secret_hash))
    conn.commit()
    cur.close()
    conn.close()
