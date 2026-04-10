import flet as ft
import requests
from api import API_URL
from router import route
from chat import setup_chat

def main(page: ft.Page):
    page.title = "MMPass"
    page.padding = 0
    page.spacing = 0
    page.window_full_screen = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.assets_dir = "assets"

    fundo_mestre = ft.Container(
        expand=True,
        bgcolor="#F8FAFC",
    )

    app_view = ft.Column(
        expand=True,
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        width=float("inf"),
    )

    fundo_mestre.content = app_view
    page.add(fundo_mestre)

    try:
        eventos_data = requests.get(API_URL).json()
        setattr(page, 'eventos', eventos_data)
    except:
        setattr(page, 'eventos', [])

    setattr(page, 'usuario_logado', None)
    setattr(page, 'carrinho', [])
    setattr(page, 'cupons_resgatados', [])
    
    setup_chat(page, app_view, route)

    route(page, app_view, "login")

if __name__ == "__main__":
    ft.app(target=main)
