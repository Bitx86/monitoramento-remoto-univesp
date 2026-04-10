import logging
import time
from logging.handlers import RotatingFileHandler
from flask import Flask, request, g

from app.routes.auth import auth_bp
from app.routes.devices import devices_bp
from app.routes.temperature import temperature_bp
from app.routes.main     import main_bp
from app.routes.dashboard   import dashboard_bp
from app.routes.historico   import historico_bp
from app.extensions.limiter     import limiter



from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 100

# ----------------------
# logging para arquivo
# ----------------------

handler = RotatingFileHandler(
    "/var/log/vacinas/vacinas.log",
    maxBytes=2_000_000,
    backupCount=10
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

limiter.init_app(app)


load_dotenv()

app.config["DB_USER"] = os.getenv("DB_USER")
app.config["DB_DB"]   = os.getenv("DB_DB")
app.config["DB_PASS"] = os.getenv("DB_PASS")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["CHAVE_CRIPTOGRAFIA"] = os.getenv("CHAVE_CRIPTOGRAFIA")
app.config["URL_SITE"] = os.getenv("URL_SITE")
app.config["LISTEN_PORT"] = os.getenv("LISTEN_PORT")
app.config["DB_HOST"] = os.getenv("DB_HOST")

app.register_blueprint(auth_bp)
app.register_blueprint(devices_bp)
app.register_blueprint(temperature_bp)
app.register_blueprint(main_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(historico_bp)


# ----------------------
# log de request
# ----------------------

@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def log_request(response):

    duration = time.time() - g.start

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    method = request.method
    path = request.path
    status = response.status_code

    app.logger.info(
        f"{ip} {method} {path} {status} {duration:.3f}s"
    )
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["LISTEN_PORT"], debug=False)
