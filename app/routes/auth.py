from flask import Blueprint, request, jsonify, render_template, request, g
from uuid import uuid4
from app.repositories.user_repository import get_user_by_email, create_user
from app.utils.hash_utils import hash_password, check_password
from app.utils.auth_utils import create_jwt
from app.utils.criptografias import descriptografar
from app.utils.iat           import gerar_token
from app.extensions.limiter  import limiter
from os import getenv
import jwt

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.before_app_request
def load_user():
    token = request.cookies.get('access_token')
    g.user = None
    if token:
        try:
            # Decodifica aqui uma única vez para a requisição inteira
            g.user = jwt.decode(token, getenv("SECRET_KEY"), algorithms=["HS256"])
        except Exception:
            pass

@auth_bp.route("/login", methods=["GET"])
def show_login():
    # Isso vai procurar o arquivo app/templates/login.html
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)
    if not user or not check_password(password, user["password_hash"]):
        return jsonify({"error": "Email ou senha incorretos"}), 401

    token = create_jwt(user["id"], user["role"])
    return jsonify({"access_token": token})

@auth_bp.route("/signup", methods=["GET"])
def show_signup():
    token = gerar_token()     #Gera um token jwt com campo "iat" contendo o time atual
    return render_template("signup.html", token=token)

@auth_bp.route("/signup", methods=["POST"])
@limiter.limit("5 per minute")
def signup():
    # Pega o token da URL (?token=...)
    #token = request.args.get("token")
    
    #if not token:
    #    return jsonify({"error": "Acesso negado. Token de convite obrigatório."}), 403

    #try:
    #    # Valida o token
    #    data_token = jwt.decode(token, getenv("SECRET_KEY"), algorithms=["HS256"])
    #    if data_token.get("type") != "registration_invite":
    #        raise jwt.InvalidTokenError
    #except jwt.ExpiredSignatureError:
    #    return jsonify({"error": "Este convite expirou."}), 401
    #except jwt.InvalidTokenError:
    #    return jsonify({"error": "Token de convite inválido."}), 401

    # Se chegou aqui, o token é válido. Agora processamos o JSON do corpo.
    data = request.get_json()
    #email = data.get("email").strip()
    #email_jwt = descriptografar(data_token["invite_email"])
    # Segurança extra: O email do cadastro deve ser o mesmo do convite?
    #if email != email_jwt:
    #    return jsonify({"error": "Este convite não foi emitido para este email."}), 403

    email     = data.get("email")

    if get_user_by_email(email):
        return jsonify({"error": "Email já cadastrado"}), 400
    
    senha     = data.get("senha")
    nome      = data.get("nome")
    sobrenome = data.get("sobrenome") 
    

    if not senha or senha.strip() == "" or len(senha) < 8:
        return jsonify({"error": "Senha menor que 8 caracteres."}), 400

    hashed_pw = hash_password(senha)
    user_id = create_user(nome, sobrenome, email, hashed_pw)
    return jsonify({"message": "Usuário criado com sucesso", "user_id": user_id})


