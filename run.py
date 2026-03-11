from flask import Flask
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["LISTEN_PORT"], debug=False)
