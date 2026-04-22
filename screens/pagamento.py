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
    total_geral = subtotal + taxa # Simplificado para o exemplo, ignorando cupons por enquanto ou pegando o valor final

    metodo_selecionado = ft.Ref[ft.Text]()

    def fechar_animacao(dialog):
        dialog.open = False
        page.update()

    def animacao_sucesso():
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320,
                height=320,
                padding=20,
                border_radius=25,
                bgcolor="surface",
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=90),
                        ft.Text("Pagamento Confirmado!", size=24, weight="bold"),
                        ft.Text("Seus ingressos já estão disponíveis.", text_align="center"),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Ver Meus Ingressos",
                            on_click=lambda _: (fechar_animacao(dialog), route(page, app_view, "ingressos"))
                        )
                    ]
                )
            )
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def processar_pagamento(e):
        if not usuario_logado:
            show_msg(page, "Erro: Usuário não identificado", bgcolor="red")
            return

        # Simulação de processamento
        btn_pagar.disabled = True
        btn_pagar.text = "Processando..."
        page.update()
        
        # Chamada para API para cada item (mantendo lógica anterior)
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
            show_msg(page, "Erro ao processar alguns itens. Tente novamente.", bgcolor="red")
            btn_pagar.disabled = False
            btn_pagar.text = "Confirmar Pagamento"
            page.update()

    # UI do Pix
    chave_pix = "pix-mmpass-0123456789"
    qr_pix = gerar_qr(chave_pix)
    ui_pix = ft.Column(
        visible=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Aponte a câmera para o QR Code", size=14, color="on_surface_variant"),
            ft.Container(
                padding=10, bgcolor="white", border_radius=15,
                content=ft.Image(src=qr_pix, width=200, height=200)
            ),
            ft.TextButton(
                "Copiar código Pix", 
                icon=ft.Icons.COPY,
                on_click=lambda _: page.set_clipboard(chave_pix)
            )
        ]
    )

    # UI do Cartão
    ui_cartao = ft.Column(
        visible=False,
        spacing=15,
        controls=[
            ft.TextField(label="Número do Cartão", placeholder="0000 0000 0000 0000", border_radius=10),
            ft.TextField(label="Nome no Cartão", placeholder="Como está no cartão", border_radius=10),
            ft.Row([
                ft.TextField(label="Validade", placeholder="MM/AA", expand=1, border_radius=10),
                ft.TextField(label="CVV", placeholder="123", expand=1, border_radius=10),
            ])
        ]
    )

    def mudar_metodo(e):
        is_pix = e.control.value == "pix"
        ui_pix.visible = is_pix
        ui_cartao.visible = not is_pix
        page.update()

    opcoes_pagamento = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="pix", label="Pix"),
            ft.Radio(value="cartao", label="Cartão de Crédito"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        value="pix",
        on_change=mudar_metodo
    )

    btn_pagar = ft.ElevatedButton(
        "Confirmar Pagamento",
        icon=ft.Icons.CHECK,
        width=float("inf"),
        height=55,
        style=ft.ButtonStyle(
            bgcolor="#818cf8", color="white",
            shape=ft.RoundedRectangleBorder(radius=15)
        ),
        on_click=processar_pagamento
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                # Header
                ft.Container(
                    padding=20,
                    content=ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: route(page, app_view, "carrinho")),
                        ft.Text("Pagamento", size=24, weight="bold", expand=True),
                    ])
                ),
                # Conteúdo
                ft.Container(
                    expand=True, padding=20,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=30,
                        controls=[
                            # Resumo
                            ft.Container(
                                padding=20, border_radius=20, bgcolor="surface_variant",
                                content=ft.Row([
                                    ft.Text("Total a pagar:", size=16),
                                    ft.Text(f"R$ {total_geral:.2f}", size=24, weight="bold", color="#818cf8")
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ),
                            # Seletor
                            ft.Column([
                                ft.Text("Selecione o método de pagamento", weight="bold"),
                                opcoes_pagamento
                            ]),
                            # Área Dinâmica
                            ft.AnimatedSwitcher(
                                content=ft.Column([ui_pix, ui_cartao]),
                                transition=ft.AnimatedSwitcherTransition.SCALE,
                            ),
                            # Botão Final
                            btn_pagar,
                            ft.Container(height=40)
                        ]
                    )
                )
            ]
        )
    )
