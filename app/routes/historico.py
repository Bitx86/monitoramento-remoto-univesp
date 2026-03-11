from flask import Blueprint, request, jsonify, render_template, request, g
historico_bp = Blueprint('historico', __name__)

@historico_bp.route("/api/dados-grafico")
def get_dados():
    # Exemplo de 30 valores aleatórios ou reais
    import random
    dados = [random.randint(10, 100) for _ in range(30)]
    return {"valores": dados}