import flet as ft
import requests
from api import API_MEUS_INGRESSOS
from utils import gerar_qr

def render_ingressos(page, app_view, route):
    usuario_logado = getattr(page, 'usuario_logado', None)
    
    if usuario_logado is None:
        page.snack_bar = ft.SnackBar(ft.Text("Faça login primeiro"))
        page.snack_bar.open = True
        page.update()
        return

    try:
        response = requests.get(f"{API_MEUS_INGRESSOS}&usuario_id={usuario_logado['id']}")
        ingressos = response.json() if response.status_code == 200 else []
    except:
        ingressos = []

    lista_cards = []

    if not ingressos:
        lista_cards.append(
            ft.Container(
                content=ft.Text("Você ainda não possui ingressos.", size=18, color="black54"),
                margin=ft.margin.only(top=50),
                alignment=ft.Alignment(0, 0) 
            )
        )

    for ingresso in ingressos:
        qr = gerar_qr(f"ingresso-{ingresso['ingresso_id']}")
        
        card = ft.Container(
            margin=ft.margin.only(bottom=20, left=10, right=10),
            padding=0, 
            border_radius=25,
            bgcolor=ft.Colors.WHITE, 
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Row(
                spacing=0,
                controls=[
                    ft.Container(width=15, bgcolor=ft.Colors.PURPLE_600),
                    ft.Container(
                        padding=20,
                        expand=True,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Text(
                                    ingresso["nome"].upper(),
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color="black",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Divider(height=1, color="black12"),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color="grey"),
                                        ft.Text(f"{ingresso['data']}", size=13, color="grey700"),
                                        ft.VerticalDivider(width=10),
                                        ft.Icon(ft.Icons.LOCATION_ON, size=16, color="grey"),
                                        ft.Text(f"{ingresso['local']}", size=13, color="grey700"),
                                    ]
                                ),
                                ft.Container(
                                    padding=10,
                                    border=ft.border.all(1, "black12"),
                                    border_radius=15,
                                    bgcolor="#f5f5f5",
                                    content=ft.Image(
                                        src=qr,
                                        width=180,
                                        height=180,
                                    )
                                ),
                                ft.Text(
                                    f"ID DO INGRESSO: #{ingresso['ingresso_id']}",
                                    size=10,
                                    color="grey",
                                    weight=ft.FontWeight.W_300
                                )
                            ]
                        )
                    )
                ]
            )
        )
        lista_cards.append(card)

    top_bar_ingressos = ft.Container(
        padding=15, 
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    bgcolor="white",
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="black",
                        on_click=lambda e: route(page, app_view, "home")
                    )
                ),
                ft.Text("Meus Ingressos", size=24, weight=ft.FontWeight.BOLD, color="black"),
                ft.IconButton(icon=ft.Icons.MORE_VERT, icon_color="black"),
            ]
        )
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                top_bar_ingressos,
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=lista_cards
                )
            ]
        )
    )
