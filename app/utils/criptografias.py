from os import getenv
from cryptography.fernet import Fernet

cipher_suite = Fernet(getenv("CHAVE_CRIPTOGRAFIA"))

def criptografar(texto):
    return cipher_suite.encrypt(texto.encode()).decode()

def descriptografar(texto_criptografado):
    return cipher_suite.decrypt(texto_criptografado.encode()).decode()