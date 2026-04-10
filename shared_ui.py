import flet as ft

def get_bottom_bar(page, app_view, route):
    return ft.Container(
        height=70,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.BLACK12)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.HOME,
                    icon_size=28,
                    on_click=lambda e: route(page, app_view, "home"),
                ),
                ft.IconButton(
                    icon=ft.Icons.CONFIRMATION_NUMBER,
                    icon_size=28,
                    on_click=lambda e: route(page, app_view, "cupons"),
                ),
                ft.IconButton(
                    icon=ft.Icons.PERSON,
                    icon_size=28,
                    on_click=lambda e: route(page, app_view, "perfil"),
                ),
            ],
        ),
    )

def card_evento(evento, page, app_view, route, largura=250):
    img_url = evento.get("imagem") or evento.get("Imagem") or "https://via.placeholder.com/150"

    return ft.Container(
        width=largura, 
        margin=ft.margin.only(left=10, right=10, top=10, bottom=10),
        padding=15,
        border_radius=20,
        bgcolor=ft.Colors.WHITE, 
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 5)),
        content=ft.GestureDetector(
            on_tap=lambda e, ev=evento: route(page, app_view, "evento", evento=ev),
            content=ft.Column(
                tight=True, 
                spacing=8,
                controls=[
                    ft.Container(
                        height=120, 
                        border_radius=15,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(
                            src=img_url,
                            fit="cover",
                            width=float("inf"), 
                        )
                    ),
                    ft.Text(
                        evento["nome"], 
                        weight="bold", 
                        size=16, 
                        color="black",
                        max_lines=1, 
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    ft.Text(
                        f'{evento["data"]} • {evento["local"]}',
                        size=11,
                        color="#444444",
                    ),
                    ft.Text(
                        f'R$ {evento["preco"]}',
                        weight="bold",
                        size=14,
                        color="black",
                    ),
                ],
            ),
        ),
    )
