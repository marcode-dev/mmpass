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
        return "green"
    elif p < 80:
        return "orange"
    else:
        return "red"

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

def show_msg(page, text, color="white", bgcolor=None):
    if not bgcolor:
        bgcolor = "green600" if "sucesso" in text.lower() or "✅" in text else "surfacevariant"
    
    page.snack_bar = ft.SnackBar(
        content=ft.Text(text, color=color),
        bgcolor=bgcolor,
        action="Ok"
    )
    page.snack_bar.open = True
    page.update()

# --- Funções de Storage Seguro ---

def safe_storage_get(page, key, default=None):
    try:
        if hasattr(page, "client_storage") and page.client_storage:
            val = page.client_storage.get(key)
            return val if val is not None else default
    except Exception as e:
        print(f"Erro ao ler storage: {e}")
    return default

def safe_storage_set(page, key, value):
    try:
        if hasattr(page, "client_storage") and page.client_storage:
            page.client_storage.set(key, value)
            return True
    except Exception as e:
        print(f"Erro ao salvar no storage: {e}")
    return False

def safe_storage_remove(page, key):
    try:
        if hasattr(page, "client_storage") and page.client_storage:
            page.client_storage.remove(key)
            return True
    except Exception as e:
        print(f"Erro ao remover do storage: {e}")
    return False
