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

def create_device(user_id, name):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (user_id, nome)
        VALUES (%s, %s)
    """, (user_id, nome))
    conn.commit()
    cur.close()
    conn.close()
