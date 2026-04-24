"""
Tela de Eventos Favoritos.
Consulta os IDs favoritados localmente e renderiza a lista a partir do servidor.
"""
import flet as ft
from shared_ui import get_bottom_bar, card_evento

def render_favoritos(page, app_view, route):
    app_view.scroll = None
    app_view.expand = True

    eventos_todos = getattr(page, 'eventos', []) or []
    # Garantir que favoritos_ids seja uma lista de strings para comparação resiliente
    favoritos_ids = [str(fid) for fid in (getattr(page, 'favoritos', []) or [])]
    
    # Filtrar apenas os eventos que são favoritos
    vistos = set()
    eventos_favoritos = []
    for e in eventos_todos:
        eid_str = str(e.get("id"))
        if eid_str in favoritos_ids and eid_str not in vistos:
            eventos_favoritos.append(e)
            vistos.add(eid_str)

    # Header Top
    header = ft.Container(
        padding=ft.padding.only(top=50, left=20, right=20, bottom=20),
        bgcolor="surface",
        content=ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_size=20, on_click=lambda _: route(page, app_view, "perfil")),
            ft.Text("Meus Favoritos", size=22, weight="bold", expand=True, text_align="center"),
            ft.Container(width=40) # Balance header
        ])
    )

    if not eventos_favoritos:
        conteudo_lista = ft.Container(
            expand=True,
            padding=30,
            content=ft.Column([
                ft.Icon(ft.Icons.FAVORITE_BORDER_ROUNDED, size=60, color="on_surface_variant"),
                ft.Text("Nenhum favorito ainda", size=20, weight="bold", color="on_surface"),
                ft.Text("Explore a Home e salve os eventos que você mais gostar!", text_align="center", color="on_surface_variant"),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Explorar Eventos",
                    style=ft.ButtonStyle(bgcolor="#818cf8", color="white", shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=lambda _: route(page, app_view, "home")
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    else:
        conteudo_lista = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            controls=[card_evento(e, page, app_view, route, largura=None) for e in eventos_favoritos],
        )

    bottom_bar = get_bottom_bar(page, app_view, route)

    app_view.controls.append(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header,
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(left=10, right=10),
                    content=conteudo_lista
                ),
                bottom_bar
            ]
        )
    )
