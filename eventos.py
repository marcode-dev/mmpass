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
    carrinho_salvo = safe_storage_get(page, "carrinho_data", default=[])
    favoritos_salvos = safe_storage_get(page, "favoritos_data", default=[])
    
    setattr(page, 'usuario_logado', usuario_salvo)
    setattr(page, 'carrinho', carrinho_salvo)
    setattr(page, 'favoritos', favoritos_salvos)
    setattr(page, 'cupons_resgatados', [])

    try:
        from api import API_EVENTOS, HEADERS
        response = requests.get(f"{API_EVENTOS}?select=*", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            eventos_data = response.json()
            setattr(page, 'eventos', eventos_data)
        else:
            print(f"Erro da API Supabase: {response.text}")
            setattr(page, 'eventos', [])
    except Exception as e:
        print(f"Erro ao carregar eventos: {e}")
        setattr(page, 'eventos', [])
        # Futuro: Adicionar botão de "Tentar Novamente" na Home
    
    setup_chat(page, app_view, route)

    # Redirecionamento Inteligente
    if usuario_salvo:
        route(page, app_view, "home")
    else:
        route(page, app_view, "login")

if __name__ == "__main__":
    ft.app(target=main)
