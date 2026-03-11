from flask import Blueprint, redirect, url_for, render_template, g
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    # Se g.user existir (preenchido pelo before_app_request), vai para o dashboard
    if g.user:
        return redirect(url_for('dashboard.dashboard'))
    
    # Caso contrário, manda para o login
    return redirect(url_for('auth.show_login'))