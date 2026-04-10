import flet as ft
import requests
import random
import qrcode
import base64
from io import BytesIO
from api import API_MEUS_INGRESSOS

def obter_total_ingressos(page):
    usuario_logado = getattr(page, 'usuario_logado', None)
    if not usuario_logado:
        return 0
    try:
        response = requests.get(
            f"{API_MEUS_INGRESSOS}&usuario_id={usuario_logado['id']}"
        )
        dados = response.json()
        return len(dados)
    except:
        return 0

def cor_lotacao(percentual):
    p = float(percentual)
    if p < 50:
        return ft.Colors.GREEN
    elif p < 80:
        return ft.Colors.ORANGE
    else:
        return ft.Colors.RED

def clima_evento():
    opcoes = [
        "☀️ Ensolarado - 27°C",
        "⛅ Parcialmente nublado - 23°C",
        "🌧 Possibilidade de chuva - 20°C",
        "🌙 Noite agradável - 18°C",
    ]
    return random.choice(opcoes)

def nivel_usuario(page):
    total = obter_total_ingressos(page)
    if total < 3:
        return "Bronze", "🥉"
    elif total < 6:
        return "Prata", "🥈"
    elif total < 10:
        return "Ouro", "🥇"
    else:
        return "Diamond", "💎"

def gerar_qr(texto):
    qr = qrcode.make(texto)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"
