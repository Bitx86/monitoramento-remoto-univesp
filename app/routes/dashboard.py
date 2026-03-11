from flask import Blueprint, redirect, url_for, render_template, g

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if g.user:
        # Se funcionou, ele está logado! Mostra o dashboard
        return render_template("dashboard.html", user_role=g.user.get('role'), user_id=g.user.get('user_id'))
    else:
        return redirect(url_for('auth.show_login'))