"""
Tela de Cupons e Programa de Fidelidade.
Oferece roleta diária e sistema de resgate de descontos.
"""
import flet as ft
from utils import nivel_usuario, obter_total_ingressos

def render_cupons(page, app_view, route):
    nivel, emoji = nivel_usuario(page)
    cupons_resgatados = getattr(page, 'cupons_resgatados', None) or []

    # Configuração de Estilo por Nível (Aparência Premium)
    estilos_nivel = {
        "Bronze": {"cores": ["#A67B5B", "#8B5E3C"], "icone": ft.Icons.MILITARY_TECH_ROUNDED, "shadow": "black26"},
        "Prata": {"cores": ["#94A3B8", "#64748B"], "icone": ft.Icons.MILITARY_TECH_ROUNDED, "shadow": "black26"},
        "Ouro": {"cores": ["#FBBF24", "#D97706"], "icone": ft.Icons.MILITARY_TECH_ROUNDED, "shadow": "orange200"},
        "Diamond": {"cores": ["#22D3EE", "#0EA5E9"], "icone": ft.Icons.DIAMOND_ROUNDED, "shadow": "blue200"},
    }
    
    estilo_atual = estilos_nivel.get(nivel, estilos_nivel["Bronze"])

    from utils import safe_storage_set
    
    # Lista de cupons usados vinda do banco (carregada no eventos.py)
    cupons_usados_ids = getattr(page, 'cupons_usados', [])

    def abrir_confirmacao(nome_cupom):
        def fechar_dialog(e):
            confirmacao_dialog.open = False
            page.update()
            
        if nome_cupom not in cupons_resgatados:
            cupons_resgatados.append(nome_cupom)
            setattr(page, 'cupons_resgatados', cupons_resgatados)
            safe_storage_set(page, "cupons_resgatados", cupons_resgatados)

        confirmacao_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320, height=380, padding=25, bgcolor="surface", border_radius=30,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            padding=20, bgcolor="#FFF9C4", border_radius=50,
                            content=ft.Icon(ft.Icons.REDEEM_ROUNDED, size=50, color="#FBC02D")
                        ),
                        ft.Column([
                            ft.Text("Cupom Resgatado!", size=22, weight="bold", color="on_surface", text_align="center"),
                            ft.Text("Copie o código e use no carrinho:", size=13, color="on_surface_variant", text_align="center"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                        ft.Container(
                            bgcolor="#F1F5F9", padding=15, border_radius=12, border=ft.border.all(1, "outline_variant"),
                            content=ft.Row([
                                ft.Text(nome_cupom, size=24, weight="bold", color="#1E293B", expand=True, text_align="center"),
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ),
                        ft.ElevatedButton(
                            "Entendido", on_click=fechar_dialog,
                            width=float("inf"), height=50, bgcolor="#818cf8", color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                        )
                    ]
                )
            )
        )
        page.overlay.append(confirmacao_dialog)
        confirmacao_dialog.open = True
        page.update()

    proximo_nivel = {"Bronze": 3, "Prata": 6, "Ouro": 10, "Diamond": 10}
    meta = proximo_nivel.get(nivel, 3)
    total = obter_total_ingressos(page)

    barra = ft.ProgressBar(width=300, value=min(total / meta, 1), color="white", bgcolor="white24")

    # Lista vinda do banco (carregada no eventos.py)
    lista_regras = getattr(page, 'lista_cupons', [])

    def pode_usar(nivel_cupom):
        ordem = ["Bronze", "Prata", "Ouro", "Diamond"]
        try: return ordem.index(nivel) >= ordem.index(nivel_cupom)
        except: return False

    cards = []
    for cupom in lista_regras:
        liberado = pode_usar(cupom["nivel"])
        ja_resgatado = cupom["nome"] in cupons_resgatados
        ja_usado = cupom["id"] in cupons_usados_ids
        
        # Lógica de estados do botão
        texto_botao = "Bloqueado"
        icone_botao = ft.Icons.LOCK_ROUNDED
        cor_botao = "outline"
        desativado = True
        
        if liberado:
            if ja_usado:
                texto_botao = "Já Utilizado"
                icone_botao = ft.Icons.BLOCK_ROUNDED
                desativado = True
            elif ja_resgatado:
                texto_botao = "Ver Código"
                icone_botao = ft.Icons.VISIBILITY_ROUNDED
                desativado = False
            else:
                texto_botao = "Resgatar"
                icone_botao = ft.Icons.REDEEM_ROUNDED
                desativado = False

        card = ft.Container(
            padding=25, margin=ft.margin.symmetric(horizontal=20, vertical=10), 
            border_radius=25, bgcolor="surface",
            opacity=1 if liberado and not ja_usado else 0.6,
            shadow=ft.BoxShadow(blur_radius=15, color="black12", offset=ft.Offset(0,5)),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(cupom["nome"], size=20, weight="bold", color="on_surface"),
                            ft.Icon(ft.Icons.LOCAL_OFFER_ROUNDED, color="#818cf8", size=20)
                        ]
                    ),
                    ft.Text(f"{cupom['desconto%']}% de desconto disponível para você.", size=14, color="on_surface_variant"),
                    ft.Row([
                        ft.Container(
                            padding=ft.padding.all(5),
                            bgcolor=estilos_nivel.get(cupom['nivel'], estilos_nivel["Bronze"])["cores"][0] + "22", # 20% opacidade
                            border_radius=8,
                            content=ft.Row([
                                ft.Icon(ft.Icons.VERIFIED_ROUNDED if liberado else ft.Icons.LOCK_ROUNDED, 
                                        size=14, 
                                        color=estilos_nivel.get(cupom['nivel'], estilos_nivel["Bronze"])["cores"][1] if liberado else "on_surface_variant"),
                                ft.Text(f"{cupom['nivel']}", 
                                        size=12, 
                                        weight="bold",
                                        color=estilos_nivel.get(cupom['nivel'], estilos_nivel["Bronze"])["cores"][1] if liberado else "on_surface_variant"),
                            ], spacing=5)
                        )
                    ], spacing=5),
                    ft.Container(height=5),
                    ft.ElevatedButton(
                        texto_botao, icon=icone_botao, disabled=desativado,
                        on_click=lambda e, n=cupom["nome"]: abrir_confirmacao(n),
                        width=float("inf"), height=48,
                        style=ft.ButtonStyle(
                            bgcolor={"disabled": "surface_variant", "": estilo_atual["cores"][0]},
                            color={"disabled": "on_surface_variant", "": "white"},
                            shape=ft.RoundedRectangleBorder(radius=12)
                        )
                    )
                ]
            )
        )
        cards.append(card)

    dashboard_status = ft.Container(
        padding=25,
        margin=15,
        border_radius=25,
        gradient=ft.LinearGradient(
            colors=estilo_atual["cores"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        shadow=ft.BoxShadow(blur_radius=25, color=estilo_atual["shadow"], offset=ft.Offset(0,10)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    ft.Icon(estilo_atual["icone"], color="white70", size=18),
                    ft.Text("Nível do Membro", size=14, color="white70", weight="w500"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                ft.Text(nivel, size=32, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(color="white24", height=30),
                ft.Text(f"Ingressos Comprados: {total}", color="white", weight="w500"),
                ft.Container(height=10),
                ft.ProgressBar(
                    width=250, value=min(total / meta, 1), color="white", bgcolor="white24", height=10
                ),
                ft.Container(height=8),
                ft.Text(f"Faltam {max(0, meta - total)} para subir de nível", color="white70", size=13)
            ]
        )
    )

    top_bar_fidelidade = ft.Container(
        padding=15, 
        content=ft.Row(
            controls=[
                ft.Container(
                    bgcolor="surface",
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=10, color="black12"),
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="on_surface",
                        on_click=lambda e: route(page, app_view, "home")
                    )
                ),
                ft.Container(width=15),
                ft.Text("Fidelidade", size=26, weight=ft.FontWeight.BOLD, color="on_surface", expand=True),
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
