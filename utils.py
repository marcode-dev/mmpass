"""
Utilitários Genéricos e Funções de Auxílio.
Agrupa métodos para gerar QRCodes, exibir mensagens (Toast), lidar com a LocalStorage e outras lógicas não atreladas à UI direta.
"""
import flet as ft
import requests
import random
import qrcode
import base64
from io import BytesIO
from api import API_INGRESSOS, HEADERS

def obter_total_ingressos(page):
    usuario_logado = getattr(page, 'usuario_logado', None)
    if not usuario_logado:
        return 0
    try:
        url = f"{API_INGRESSOS}?usuario_id=eq.{usuario_logado['id']}&select=id"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return len(dados)
        return 0
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
    qr_img = qrcode.make(texto)
    buffer = BytesIO()
    qr_img.save(buffer, "PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def gerar_token(tamanho=10):
    import secrets
    import string
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

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

def sync_user_data(page):
    """Sincroniza favoritos e cupons do usuário logado com o banco de dados."""
    usuario = getattr(page, 'usuario_logado', None)
    if not usuario:
        return
        
    from api import API_FAVORITOS, API_CUPONS_USADOS, HEADERS
    user_id = usuario['id']
    
    try:
        # 1. Favoritos
        resp_favs = requests.get(f"{API_FAVORITOS}?usuario_id=eq.{user_id}&select=evento_id", headers=HEADERS, timeout=5)
        if resp_favs.status_code == 200:
            favs_ids = list(dict.fromkeys([f['evento_id'] for f in resp_favs.json()]))
            setattr(page, 'favoritos', favs_ids)
            safe_storage_set(page, "favoritos_data", favs_ids)
        
        # 2. Cupons Usados
        resp_usados = requests.get(f"{API_CUPONS_USADOS}?usuario_id=eq.{user_id}&select=cupom_id", headers=HEADERS, timeout=5)
        if resp_usados.status_code == 200:
            usados_ids = [c['cupom_id'] for c in resp_usados.json()]
            setattr(page, 'cupons_usados', usados_ids)
            
    except Exception as e:
        print(f"Erro na sincronização de dados: {e}")
