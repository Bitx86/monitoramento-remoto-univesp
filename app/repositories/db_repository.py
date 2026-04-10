import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DB_CONFIG
import logging
import jwt
import datetime
from app.utils.criptografias import criptografar
from os import getenv

def get_db_connection():
    # Centraliza a conexão para facilitar manutenção
    return psycopg2.connect(**DB_CONFIG)
