import flet as ft
from utils import cor_lotacao, clima_evento, show_msg, safe_storage_set

def render_evento(page, app_view, route, evento):
    if not evento:
        route(page, app_view, "home")
        return

    lotacao_percent = float(evento["lotacao_percentual"])
    lotacao_valor = lotacao_percent / 100
    cor = cor_lotacao(lotacao_percent)
    clima = clima_evento()

    def adicionar_carrinho(e):
        carrinho = getattr(page, 'carrinho', None) or []
        carrinho.append(evento)
        setattr(page, 'carrinho', carrinho)
        # Persistência
        safe_storage_set(page, "carrinho_data", carrinho)
        
        show_msg(page, f"Festa garantida! {evento['nome']} adicionado ao carrinho 🚀", bgcolor="#818cf8")
        
        route(page, app_view, "carrinho")

    # Header Hero com Stack
    hero_section = ft.Stack(
        controls=[
            ft.Container(
                height=350,
                content=ft.Image(
                    src=evento.get("imagem", ""),
                    fit="cover",
                    width=float("inf"),
                ),
            ),
            # Gradiente de sobreposição para leitura
            ft.Container(
                height=350,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, 0.5),
                    end=ft.Alignment(0, 1),
                    colors=["transparent", "#cc000000"],
                ),
            ),
            # Botão de Voltar Flutuante
            ft.Container(
                top=40,
                left=20,
                content=ft.Container(
                    bgcolor="#33ffffff",
                    blur=ft.Blur(10, 10),
                    border_radius=15,
                    padding=5,
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                        icon_color="white",
                        icon_size=20,
                        on_click=lambda e: route(page, app_view, "home")
                    ),
                ),
            ),
        ]
    )

    # Conteúdo Detalhado
    content_section = ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=100),
        content=ft.Column(
            spacing=25,
            controls=[
                # Título e Preço
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(evento["nome"], size=30, weight=ft.FontWeight.BOLD, color="on_surface"),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, size=16, color="#818cf8"),
                            ft.Text(evento["local"], size=14, color="on_surface_variant"),
                        ]),
                    ]
                ),
                
                # Cards de Info Rápida
                ft.Row(
                    spacing=15,
                    controls=[
                        ft.Container(
                            expand=1,
                            padding=15,
                            bgcolor="surface_variant",
                            border_radius=15,
                            content=ft.Column([
                                ft.Icon(ft.Icons.CALENDAR_MONTH, color="#818cf8"),
                                ft.Text("Data", size=12, color="on_surface_variant"),
                                ft.Text(evento["data"], size=14, weight="bold"),
                            ], spacing=5)
                        ),
                        ft.Container(
                            expand=1,
                            padding=15,
                            bgcolor="surface_variant",
                            border_radius=15,
                            content=ft.Column([
                                ft.Icon(ft.Icons.THERMOSTAT, color="#f87171"),
                                ft.Text("Clima", size=12, color="on_surface_variant"),
                                ft.Text(clima, size=14, weight="bold"),
                            ], spacing=5)
                        ),
                    ]
                ),

                # Lotação
                ft.Container(
                    padding=20,
                    bgcolor="surface",
                    border=ft.border.all(1, "outline_variant"),
                    border_radius=20,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Disponibilidade", weight="bold"),
                            ft.Text(f"{evento['lotacao_percentual']}%", color=cor, weight="bold"),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=lotacao_valor, color=cor, bgcolor="outline_variant", height=8),
                        ft.Text("Garanta o seu antes que esgote!", size=12, color="on_surface_variant"),
                    ], spacing=10)
                ),

                # Descrição (Placeholder profissional)
                ft.Column([
                    ft.Text("Sobre o Evento", size=18, weight="bold"),
                    ft.Text(
                        f"Prepare-se para uma experiência inesquecível em {evento['local']}. "
                        "Este evento exclusivo traz o melhor do entretenimento com segurança e conforto garantidos pela MMPass. "
                        "Não perca a chance de fazer parte deste momento único.",
                        color="on_surface_variant"
                    ),
                ], spacing=10),
            ]
        )
    )

    # Barra de Compra Fixa (Botão Stick no Rodapé)
    action_bar = ft.Container(
        bottom=0,
        left=0,
        right=0,
        padding=ft.padding.only(left=25, right=25, top=15, bottom=25),
        bgcolor=ft.Colors.with_opacity(0.9, "surface"),
        blur=ft.Blur(10, 10),
        border=ft.border.only(top=ft.border.BorderSide(1, "outline_variant")),
        content=ft.Row([
            ft.Column([
                ft.Text("Preço unitário", size=12, color="on_surface_variant"),
                ft.Text(f"R$ {evento['preco']}", size=22, weight="bold", color="on_surface"),
            ], spacing=2, expand=True),
            ft.Container(
                gradient=ft.LinearGradient(colors=["#93c5fd", "#818cf8"]),
                border_radius=15,
                content=ft.ElevatedButton(
                    "Adicionar ao Carrinho",
                    color="white",
                    bgcolor=ft.Colors.TRANSPARENT,
                    elevation=0,
                    width=200,
                    height=50,
                    on_click=adicionar_carrinho,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                    )
                ),
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # Montando a View
    app_view.controls.append(
        ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=0,
                    controls=[
                        hero_section,
                        content_section
                    ]
                ),
                action_bar
            ]
        )
    )
