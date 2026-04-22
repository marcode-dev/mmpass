import flet as ft

def get_bottom_bar(page, app_view, route):
    return ft.Container(
        height=70,
        bgcolor="surface",
        border=ft.border.only(top=ft.border.BorderSide(1, "outline_variant")),
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
        margin=ft.margin.all(10),
        padding=15,
        border_radius=20,
        bgcolor="surface", 
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 5)),
        animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
        on_hover=lambda e: setattr(e.control, "scale", 1.02 if e.data == "true" else 1.0),
        on_click=lambda e: route(page, app_view, "evento", evento=evento),
        content=ft.Column(
            tight=True, 
            spacing=8,
            controls=[
                ft.Container(
                    height=140, 
                    border_radius=15,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Image(
                        src=img_url,
                        fit="cover",
                        width=float("inf"),
                        cache_width=400,
                    )
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            expand=True,
                            spacing=2,
                            controls=[
                                ft.Text(
                                    evento["nome"], 
                                    weight="bold", 
                                    size=16, 
                                    color="on_surface",
                                    max_lines=1, 
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Row([
                                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=12, color="on_surface_variant"),
                                    ft.Text(f'{evento["data"]} • {evento["local"]}', size=11, color="on_surface_variant"),
                                ], spacing=5),
                            ]
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f'R$ {evento["preco"]}', weight="bold", size=16, color="on_surface"),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            bgcolor="#1a818cf8",
                            border_radius=10,
                            content=ft.Text("Ver Ingressos", size=10, weight="bold", color="#818cf8")
                        )
                    ]
                ),
            ],
        ),
    )
