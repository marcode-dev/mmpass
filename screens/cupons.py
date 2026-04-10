import flet as ft
from utils import nivel_usuario, obter_total_ingressos

def render_cupons(page, app_view, route):
    nivel, emoji = nivel_usuario(page)
    cupons_resgatados = getattr(page, 'cupons_resgatados', None) or []

    def abrir_confirmacao(nome_cupom):
        def fechar_dialog(e):
            confirmacao_dialog.open = False
            page.update()
            
        if nome_cupom not in cupons_resgatados:
            cupons_resgatados.append(nome_cupom)
            setattr(page, 'cupons_resgatados', cupons_resgatados)

        confirmacao_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320,
                height=400,
                padding=20,
                bgcolor="white",
                border_radius=25,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Icon(ft.Icons.REDEEM, size=70, color="#FF9D00"),
                        ft.Text("Cupom Resgatado!", size=22, weight="bold"),
                        ft.Text("Use o código abaixo na compra:", color="black54", text_align="center"),
                        ft.Container(
                            bgcolor="#FFF5F0",
                            padding=15,
                            border_radius=10,
                            content=ft.Text(nome_cupom, size=28, weight="bold", color="#E64A19")
                        ),
                        ft.Button(
                            content=ft.Text("Fechar"), 
                            on_click=fechar_dialog,
                            width=200,
                            bgcolor="black",
                            color="white"
                        )
                    ]
                )
            )
        )
        page.overlay.append(confirmacao_dialog)
        confirmacao_dialog.open = True
        page.update()

    proximo_nivel = {
        "Bronze": 3,
        "Prata": 6,
        "Ouro": 10,
        "Diamond": 10
    }

    meta = proximo_nivel[nivel]
    total = obter_total_ingressos(page)

    barra = ft.ProgressBar(
        width=300,
        value=min(total / meta, 1),
        color="white",
        bgcolor="white24"
    )

    cupons = [
        {"nome": "MAKO5", "desc": "R$5 de desconto", "nivel": "Bronze"},
        {"nome": "MAKO10", "desc": "10% OFF em eventos", "nivel": "Prata"},
        {"nome": "VIP20", "desc": "20% OFF eventos VIP", "nivel": "Ouro"},
        {"nome": "DIAMOND30", "desc": "30% OFF + acesso antecipado", "nivel": "Diamond"},
    ]

    def pode_usar(nivel_cupom):
        ordem = ["Bronze","Prata","Ouro","Diamond"]
        return ordem.index(nivel) >= ordem.index(nivel_cupom)

    cards = []
    for cupom in cupons:
        liberado = pode_usar(cupom["nivel"])
        card = ft.Container(
            padding=20,
            margin=15,
            width=320,
            border_radius=20,
            bgcolor="white",
            opacity=1 if liberado else 0.5,
            shadow=ft.BoxShadow(blur_radius=12, color="black12", offset=ft.Offset(0,4)),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(cupom["nome"], size=20, weight=ft.FontWeight.BOLD),
                            ft.Icon(ft.Icons.LOCAL_OFFER, color="#8ca6db")
                        ]
                    ),
                    ft.Text(cupom["desc"], size=15, color="black87"),
                    ft.Text(f"Nível necessário: {cupom['nivel']}", size=13, color="black54"),
                    ft.Container(height=5),
                    ft.Button(
                        "Resgatar" if liberado else "Bloqueado",
                        icon=ft.Icons.REDEEM if liberado else ft.Icons.LOCK,
                        disabled=not liberado,
                        on_click=lambda e, n=cupom["nome"]: abrir_confirmacao(n), 
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=15)
                    )
                ]
            )
        )
        cards.append(card)

    dashboard_status = ft.Container(
        padding=25,
        margin=15,
        border_radius=20,
        gradient=ft.LinearGradient(
            colors=["#93c5fd", "#818cf8"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.PURPLE_200, offset=ft.Offset(0,10)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Nível do Membro", size=14, color="white70"),
                ft.Text(nivel, size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(color="white24"),
                ft.Text(f"Ingressos Comprados: {total}", color="white"),
                ft.Container(height=10),
                ft.ProgressBar(
                    width=250, value=min(total / meta, 1), color="white", bgcolor="white24", height=8
                ),
                ft.Container(height=5),
                ft.Text(f"Faltam {max(0, meta - total)} para subir de nível", color="white70", size=12)
            ]
        )
    )

    top_bar_fidelidade = ft.Container(
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
                ft.Container(width=15),
                ft.Text("Fidelidade", size=26, weight=ft.FontWeight.BOLD, color="black", expand=True),
            ]
        )
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                top_bar_fidelidade,
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        dashboard_status,
                        ft.Container(height=10),
                        *cards
                    ]
                )
            ]
        )
    )
