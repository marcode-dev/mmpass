"""
Ponto de entrada principal da aplicação (App Entrypoint).
Inicializa a janela do Flet, gerencia a hidratação de sessão persistente e invoca o roteador raiz.
"""
import flet as ft
import requests
from router import route
from chat import setup_chat
from utils import safe_storage_get

def main(page: ft.Page):
    page.title = "MMPass"
    page.padding = 0
    page.spacing = 0
    page.window_full_screen = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="#818cf8")
    page.dark_theme = ft.Theme(color_scheme_seed="#818cf8")
    page.assets_dir = "assets"

    fundo_mestre = ft.Container(
        expand=True,
    )

    app_view = ft.Column(
        expand=True,
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        width=float("inf"),
    )

    fundo_mestre.content = app_view
    
    
    page.add(fundo_mestre)

    # Inicialização de dados persistentes
    usuario_salvo = safe_storage_get(page, "usuario_logado")
    # Inicialização de dados persistentes do Carrinho
    carrinho_salvo = safe_storage_get(page, "carrinho_data", default=[])
    setattr(page, 'usuario_logado', usuario_salvo)
    setattr(page, 'carrinho', carrinho_salvo)
    
    # Inicialização de cupons resgatados (UI/Visual apenas)
    resgatados_salvos = safe_storage_get(page, "cupons_resgatados", default=[])
    setattr(page, 'cupons_resgatados', resgatados_salvos)

    try:
        from api import API_EVENTOS, API_CUPONS, API_FAVORITOS, API_CUPONS_USADOS, HEADERS
        
        # 1. Carregar Eventos Globais
        response = requests.get(f"{API_EVENTOS}?select=*", headers=HEADERS, timeout=10)
        setattr(page, 'eventos', response.json() if response.status_code == 200 else [])

        # 2. Carregar Regras de Cupons Globais
        resp_cupons = requests.get(f"{API_CUPONS}?select=*", headers=HEADERS, timeout=10)
        setattr(page, 'lista_cupons', resp_cupons.json() if resp_cupons.status_code == 200 else [])

        # 3. Sincronização de Dados do Usuário
        from utils import sync_user_data
        sync_user_data(page)
            
    except Exception as e:
        print(f"Erro ao sincronizar dados iniciais: {e}")
        setattr(page, 'eventos', [])
        setattr(page, 'lista_cupons', [])
        setattr(page, 'favoritos', [])
        setattr(page, 'cupons_usados', [])
    
    setup_chat(page, app_view, route)

    # Redirecionamento Inteligente
    if usuario_salvo:
        route(page, app_view, "home")
    else:
        route(page, app_view, "login")

if __name__ == "__main__":
    ft.app(target=main)
