import flet as ft
from utils import cor_lotacao, clima_evento

def render_evento(page, app_view, route, evento):
    if not evento:
        route(page, app_view, "home")
        return

    lotacao_percent = float(evento["lotacao_percentual"])
    lotacao_valor = lotacao_percent / 100
    cor = cor_lotacao(lotacao_percent)
    clima = clima_evento()

    def adicionar_carrinho(evt):
        carrinho = getattr(page, 'carrinho', None) or []
        carrinho.append(evt)
        setattr(page, 'carrinho', carrinho)
        page.snack_bar = ft.SnackBar(ft.Text("Ingresso adicionado ao carrinho 🛒"))
        page.snack_bar.open = True
        route(page, app_view, "carrinho")

    top_bar_evento = ft.Container(
        padding=15, 
        content=ft.Row(
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
                ft.Container(width=10),
                ft.Text("Detalhes", size=26, weight=ft.FontWeight.BOLD, color="black"),
            ]
        )
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                top_bar_evento,
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(
                            height=220,
                            margin=15,
                            border_radius=20,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=evento.get("imagem", ""),
                                fit="cover"
                            ),
                        ),
                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    ft.Text(evento["nome"], size=24, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Text(f'{evento["data"]} • {evento["local"]}', color="black87"),
                                    ft.Text(f'R$ {evento["preco"]}', size=20, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Divider(color="black12"),
                                    ft.Text("Clima previsto no dia:", weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Text(clima, color="black87"),
                                    ft.Divider(color="black12"),
                                    ft.Text("Lotação em tempo real", weight=ft.FontWeight.BOLD, color="black"),
                                    ft.ProgressBar(value=lotacao_valor, color=cor),
                                    ft.Text(f"{evento['lotacao_percentual']}% ocupado", color="black87"),
                                    ft.Container(height=10),
                                    ft.Button(
                                        "Adicionar ao carrinho",
                                        icon=ft.Icons.SHOPPING_CART,
                                        on_click=lambda e: adicionar_carrinho(evento)
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            ]
        )
    )
