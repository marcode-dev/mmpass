import flet as ft
import requests
from api import API_URL_COMPRAR
from utils import show_msg, gerar_qr, safe_storage_set

def render_pagamento(page, app_view, route):
    carrinho = getattr(page, 'carrinho', None) or []
    usuario_logado = getattr(page, 'usuario_logado', None)
    
    if not carrinho:
        route(page, app_view, "home")
        return

    subtotal = sum(float(ev["preco"]) for ev in carrinho)
    taxa = 15.00
    total_geral = subtotal + taxa

    # Estado local da tela
    metodo_atual = "pix" # Padrão

    def abrir_dialogo(dialog):
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def fechar_dialogo(dialog):
        dialog.open = False
        page.update()

    def animacao_sucesso():
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320,
                height=350,
                padding=20,
                border_radius=25,
                bgcolor="surface",
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=100, height=100,
                            bgcolor="#f0fdf4",
                            border_radius=50,
                            alignment=ft.Alignment(0,0),
                            content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="green", size=60)
                        ),
                        ft.Container(height=10),
                        ft.Text("Pagamento Confirmado!", size=22, weight="bold", color="on_surface"),
                        ft.Text("Seus ingressos digitais já foram gerados.", text_align="center", color="on_surface_variant"),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Acessar Meus Ingressos",
                            width=240,
                            height=50,
                            style=ft.ButtonStyle(bgcolor="#818cf8", color="white", shape=ft.RoundedRectangleBorder(radius=12)),
                            on_click=lambda _: (fechar_dialogo(dialog), route(page, app_view, "ingressos"))
                        )
                    ]
                )
            )
        )
        abrir_dialogo(dialog)

    def processar_pagamento(e):
        if not usuario_logado:
            show_msg(page, "Erro: Faça login para continuar", bgcolor="red")
            return

        btn_pagar.disabled = True
        btn_pagar.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
        page.update()
        
        sucesso_total = True
        for evento in carrinho:
            try:
                dados = {
                    "action": "comprar",
                    "usuario_id": usuario_logado["id"],
                    "evento_id": evento["id"]
                }
                response = requests.post(API_URL_COMPRAR, json=dados, timeout=10)
                if response.json().get("status") != "sucesso":
                    sucesso_total = False
            except:
                sucesso_total = False
        
        if sucesso_total:
            carrinho.clear()
            safe_storage_set(page, "carrinho_data", [])
            animacao_sucesso()
        else:
            show_msg(page, "Falha no processamento. Verifique seus dados.", bgcolor="red")
            btn_pagar.disabled = False
            btn_pagar.content = ft.Text("Tentar Novamente", weight="bold")
            page.update()

    # UI do Pix
    chave_pix = "pix-mmpass-0123456789"
    qr_pix = gerar_qr(chave_pix)
    ui_pix = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Container(
                padding=20,
                bgcolor="white",
                border_radius=25,
                border=ft.border.all(1, "outline_variant"),
                shadow=ft.BoxShadow(blur_radius=20, color="black12"),
                content=ft.Image(src=qr_pix, width=220, height=220)
            ),
            ft.Column([
                ft.Text("Escaneie o código acima ou copie a chave:", size=13, color="on_surface_variant", text_align="center"),
                ft.Container(
                    padding=15,
                    bgcolor="#f8fafc",
                    border_radius=12,
                    on_click=lambda _: page.set_clipboard(chave_pix),
                    content=ft.Row([
                        ft.Text(chave_pix, size=13, weight="bold", color="on_surface", expand=True),
                        ft.Icon(ft.Icons.COPY_ALL_ROUNDED, size=20, color="#818cf8")
                    ])
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        ]
    )

    # UI do Cartão
    ui_cartao = ft.Column(
        spacing=15,
        controls=[
            # Visual do Cartão
            ft.Container(
                height=180,
                width=float("inf"),
                border_radius=20,
                gradient=ft.LinearGradient(
                    colors=["#1e293b", "#334155"],
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1)
                ),
                padding=25,
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color="white60", size=30),
                        ft.Text("MMPass Gold", color="white60", size=12)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=20),
                    ft.Text("•••• •••• •••• ••••", color="white", size=20, weight="bold"),
                    ft.Container(height=10),
                    ft.Row([
                        ft.Column([
                            ft.Text("TITULAR", color="white60", size=10),
                            ft.Text(usuario_logado['nome'].upper() if usuario_logado else "NOME DO TITULAR", color="white", size=14)
                        ]),
                        ft.Column([
                            ft.Text("VALIDADE", color="white60", size=10),
                            ft.Text("••/••", color="white", size=14)
                        ], horizontal_alignment=ft.CrossAxisAlignment.END)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            ),
            ft.TextField(label="Número do Cartão", hint_text="0000 0000 0000 0000", border_radius=15, bgcolor="surface"),
            ft.Row([
                ft.TextField(label="Validade", hint_text="MM/AA", expand=1, border_radius=15, bgcolor="surface"),
                ft.TextField(label="CVV", hint_text="•••", expand=1, border_radius=15, bgcolor="surface"),
            ], spacing=15)
        ]
    )

    area_dinamica = ft.Container(content=ui_pix)

    def selecionar_metodo(metodo):
        nonlocal metodo_atual
        metodo_atual = metodo
        if metodo == "pix":
            area_dinamica.content = ui_pix
            btn_pix.bgcolor = "#818cf8"
            btn_pix.border = None
            text_pix.color = "white"
            icon_pix.color = "white"
            
            btn_card.bgcolor = "transparent"
            btn_card.border = ft.border.all(1, "outline_variant")
            text_card.color = "on_surface"
            icon_card.color = "#818cf8"
        else:
            area_dinamica.content = ui_cartao
            btn_card.bgcolor = "#818cf8"
            btn_card.border = None
            text_card.color = "white"
            icon_card.color = "white"
            
            btn_pix.bgcolor = "transparent"
            btn_pix.border = ft.border.all(1, "outline_variant")
            text_pix.color = "on_surface"
            icon_pix.color = "#818cf8"
        page.update()

    # Botões de Seleção Customizados
    icon_pix = ft.Icon(ft.Icons.QR_CODE_ROUNDED, color="white", size=24)
    text_pix = ft.Text("Pix", weight="bold", color="white")
    btn_pix = ft.Container(
        expand=1, height=60, bgcolor="#818cf8", border_radius=15,
        on_click=lambda _: selecionar_metodo("pix"),
        content=ft.Row([icon_pix, text_pix], alignment=ft.MainAxisAlignment.CENTER)
    )

    icon_card = ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color="#818cf8", size=24)
    text_card = ft.Text("Cartão", weight="bold", color="on_surface")
    btn_card = ft.Container(
        expand=1, height=60, border=ft.border.all(1, "outline_variant"), border_radius=15,
        on_click=lambda _: selecionar_metodo("cartao"),
        content=ft.Row([icon_card, text_card], alignment=ft.MainAxisAlignment.CENTER)
    )

    btn_pagar = ft.Container(
        content=ft.Text("Confirmar Pagamento", weight="bold", color="white", size=16),
        alignment=ft.Alignment(0, 0),
        width=float("inf"),
        height=60,
        bgcolor="#818cf8",
        border_radius=18,
        on_click=processar_pagamento,
        shadow=ft.BoxShadow(blur_radius=15, color="purple200", offset=ft.Offset(0, 5))
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Top Header
                ft.Container(
                    padding=ft.padding.only(top=50, left=20, right=20, bottom=20),
                    bgcolor="surface",
                    content=ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_size=20, on_click=lambda _: route(page, app_view, "carrinho")),
                        ft.Text("Pagamento", size=22, weight="bold", expand=True, text_align="center"),
                        ft.Container(width=40) # Balance header
                    ])
                ),
                # Conteúdo Principal
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(left=25, right=25, top=10),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=30,
                        controls=[
                            # Resumo de Compra Moderno
                            ft.Container(
                                padding=25,
                                border_radius=25,
                                bgcolor="surface",
                                border=ft.border.all(1, "outline_variant"),
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("Total da Compra", size=14, color="on_surface_variant"),
                                        ft.Text(f"R$ {total_geral:.2f}", size=24, weight="bold", color="#818cf8")
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Divider(height=30, color="outline_variant", thickness=0.5),
                                    ft.Row([
                                        ft.Text(f"{len(carrinho)} ingressos", size=14, color="on_surface_variant"),
                                        ft.Text(f"Taxa de serviço: R$ {taxa:.2f}", size=12, color="on_surface_variant")
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                ])
                            ),
                            # Seletores de Método
                            ft.Column([
                                ft.Text("Método de Pagamento", weight="bold", size=16),
                                ft.Row([btn_pix, btn_card], spacing=15)
                            ], spacing=10),
                            
                            # Área de Input Dinâmica
                            area_dinamica,
                            
                            # Rodapé com Botão
                            ft.Container(
                                padding=ft.padding.only(top=10, bottom=30),
                                content=btn_pagar
                            )
                        ]
                    )
                )
            ]
        )
    )
