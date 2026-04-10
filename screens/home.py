import flet as ft
from shared_ui import get_bottom_bar, card_evento

def render_home(page, app_view, route):
    app_view.scroll = None
    app_view.expand = True

    eventos = getattr(page, 'eventos', None) or []

    lista_vertical = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[card_evento(e, page, app_view, route, largura=None) for e in eventos],
    )

    def filtrar_eventos(texto):
        texto = texto.lower()
        lista_vertical.controls.clear()
        for e in eventos:
            if texto in e["nome"].lower():
                lista_vertical.controls.append(card_evento(e, page, app_view, route, largura=None))
        page.update()

    campo_busca = ft.TextField(
        hint_text="Pesquisar eventos...",
        expand=True,
        border_radius=30,
        border_color="transparent",
        filled=True,
        bgcolor="white",
        color="black",
        on_change=lambda e: filtrar_eventos(e.control.value)
    )

    search_bar = ft.Container(
        padding=ft.padding.only(top=40, left=15, right=15, bottom=20),
        gradient=ft.LinearGradient(
            colors=["#93c5fd", "#818cf8"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        content=ft.Row(
            spacing=15,
            controls=[
                campo_busca,
                ft.Container(
                    bgcolor="white24",
                    border_radius=15,
                    content=ft.IconButton(
                        icon=ft.Icons.SHOPPING_CART,
                        icon_color="white",
                        on_click=lambda e: route(page, app_view, "carrinho")
                    )
                )
            ],
        ),
    )

    carrossel = ft.Container(
        height=240,
        content=ft.Row(
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            controls=[card_evento(e, page, app_view, route, largura=280) for e in eventos],
        ),
    )

    bottom_bar = get_bottom_bar(page, app_view, route)

    scroll_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            search_bar,
            ft.Container(
                padding=ft.padding.only(left=15, bottom=5, top=20),
                content=ft.Row([
                    ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color="#818cf8", size=24),
                    ft.Text("Em Alta", size=20, weight=ft.FontWeight.BOLD, color="black")
                ]),
            ),
            carrossel,
            ft.Container(
                padding=ft.padding.only(left=15, top=15, bottom=5),
                content=ft.Row([
                    ft.Icon(ft.Icons.EVENT_AVAILABLE, color="#818cf8", size=24),
                    ft.Text("Outros Eventos", size=20, weight=ft.FontWeight.BOLD, color="black")
                ]),
            ),
            lista_vertical,
            ft.Container(height=20)
        ]
    )

    app_view.controls.append(scroll_content)
    app_view.controls.append(bottom_bar)
