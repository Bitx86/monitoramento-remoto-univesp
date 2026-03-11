import jwt
import datetime
import sys
import jwt
# Importando suas funções e configs
from .criptografias import criptografar
from app.config import SECRET_KEY, URL_SITE
from os import getenv

def generate_invite_token(email_destinatario):
    email_escondido = criptografar(email_destinatario)
    # Usando timezone-aware para evitar avisos de depreciação se estiver em versões novas
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    
    payload = {
        "invite_email": email_escondido,
        "exp": expiration,
        "type": "registration_invite"
    }
    
    token = jwt.encode(payload, getenv("SECRET_KEY"), algorithm="HS256")
    return token

def main():
    print("--- GERADOR DE CONVITES FKVILA ---")
    
    # Verifica se o email veio como argumento: python gerar_convite.py email@teste.com
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        # Se não veio, ele pergunta na tela
        email = input("Digite o e-mail do destinatário: ").strip()

    if not email:
        print("❌ Erro: O e-mail não pode ser vazio.")
        return

    try:
        token = generate_invite_token(email)
        link = f"{URL_SITE}/signup?token={token}"
        
        print("\n✅ Convite gerado com sucesso!")
        print(f"📧 E-mail: {email}")
        print(f"🔗 Link de Cadastro:\n\n{link}\n")
        print("⚠️  Atenção: Este link expira em 24 horas.")
        
    except Exception as e:
        print(f"❌ Ocorreu um erro ao gerar o convite: {e}")

if __name__ == "__main__":
    main()

