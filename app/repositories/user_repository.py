import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DB_CONFIG
import logging
import jwt
import datetime
from app.utils.criptografias import criptografar
from app.repositories.db_repository import get_db_connection
from os import getenv


def generate_invite_url(email_destinatario):
    email_escondido = criptografar(email_destinatario)
    expiration  = datetime.datetime.utcnoew() + datetime.timedelta(hours=24)
    payload = {
	"invite_email": email_escondido,
	"exp": expiration,
	"type":"registration_invite"
    }
    token = jwt.encode(payload, getenv("SECRET_KEY"), algorithm="HS256")
    url   = getenv("URL_SITE") + "/signup?token={token}"

    return url


def get_user_by_email(email):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE email=%s", (email,))
                return cur.fetchone()
    except Exception as e:
        logging.error(f"Erro ao buscar usuário por email: {e}")
        return None

def create_user(nome, sobrenome, email, password_hash, role="tecnicos"):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (nome, sobrenome, email, password_hash, role)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (nome, sobrenome, email, password_hash, role))
                
                user_id = cur.fetchone()[0]
                conn.commit() # Salva as alterações
                logging.info(f"Criado o usuário {nome} {email}")
                return user_id
    except psycopg2.IntegrityError:
        logging.warning(f"Tentativa de criar usuário com email duplicado: {email}")
        raise # Repassa o erro para a rota tratar
    except Exception as e:
        logging.error(f"Erro crítico no banco de dados: {e}")
        raise