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
        padding=ft.Padding(20, 35, 20, 15),
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
                    padding=ft.Padding(10, 0, 10, 0),
                    content=conteudo_lista
                ),
                bottom_bar
            ]
        )
    )

    # Lógica de Onboarding (Sistema de Hype) - Aparece se não houver favoritos
    if len(eventos_favoritos) == 0:
        from utils import safe_storage_get, safe_storage_set
        ja_viu = safe_storage_get(page, "hype_modal_v4") # Versão 4 para resetar teste
        
        if str(ja_viu) != "1":
            def fechar_guia(e):
                dialog.open = False
                page.update()
                safe_storage_set(page, "hype_modal_v4", "1")

            dialog = ft.AlertDialog(
                modal=True,
                content=ft.Container(
                    width=320, height=400, padding=20,
                    content=ft.Column([
                        ft.Container(
                            padding=20, bgcolor="purple50", border_radius=50,
                            content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, size=50, color="#818cf8")
                        ),
                        ft.Text("Impulsione o Hype! 🚀", size=22, weight="bold", text_align="center"),
                        ft.Text(
                            "Sabia que favoritar eventos impulsiona nosso 'Sistema de Hype'?\n\n"
                            "Ao favoritar, você destaca os eventos e pode receber notificações de promoções exclusivas!",
                            text_align="center", color="on_surface_variant", size=14
                        ),
                        ft.ElevatedButton(
                            "Entendi!",
                            on_click=fechar_guia,
                            width=float("inf"), height=50,
                            bgcolor="#818cf8", color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
                ),
                shape=ft.RoundedRectangleBorder(radius=30),
            )
            page.overlay.append(dialog)
            page.dialog = dialog
            dialog.open = True
            page.update()
