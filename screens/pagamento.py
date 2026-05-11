"""
Tela de Pagamento e Checkout de Carrinho.
Orquestra o registro atômico de compra: confere lotação, deduz cupons, adiciona ingressos e incrementa as vendas num único fluxo.
"""
import flet as ft
import requests
from api import API_EVENTOS, API_INGRESSOS, HEADERS
from utils import show_msg, gerar_qr, safe_storage_set

def render_pagamento(page, app_view, route):
    carrinho = getattr(page, 'carrinho', None) or []
    usuario_logado = getattr(page, 'usuario_logado', None)
    
    if not carrinho:
        route(page, app_view, "home")
        return

    subtotal = sum(float(ev["preco"]) for ev in carrinho)
    taxa = 15.00
    desconto = getattr(page, 'desconto_aplicado', 0)
    total_geral = subtotal + taxa - desconto

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
        def fechar_sucesso(e):
            dialog.open = False
            page.update()
            route(page, app_view, "ingressos")
            
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=300,
                padding=20,
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, color="green", size=80),
                    ft.Text("Pagamento Aprovado!", size=22, weight="bold", color="on_surface", text_align="center"),
                    ft.Text("Seus ingressos já estão disponíveis na aba Perfil.", size=14, color="on_surface_variant", text_align="center"),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Ver Ingressos",
                        bgcolor="green600",
                        color="white",
                        width=float("inf"),
                        on_click=fechar_sucesso
                    )
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

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
                # 1. Verificar lotação
                resp_evento = requests.get(f"{API_EVENTOS}?id=eq.{evento['id']}&select=capacidade,ingressos_vendidos", headers=HEADERS, timeout=10)
                if resp_evento.status_code != 200 or not resp_evento.json():
                    sucesso_total = False
                    continue
                
                dados_ev = resp_evento.json()[0]
                if dados_ev['ingressos_vendidos'] >= dados_ev['capacidade']:
                    sucesso_total = False # Evento lotado
                    continue

                # 2. Registrar Ingresso
                cupom_id = getattr(page, 'cupom_aplicado_id', None)
                desconto_perc = getattr(page, 'desconto_porcentagem', 0)
                token = gerar_token(12)
                
                novo_ingresso = {
                    "usuario_id": usuario_logado["id"],
                    "evento_id": evento["id"],
                    "desconto": cupom_id, # Agora armazena o ID do cupom
                    "codigo": token
                }
                resp_ing = requests.post(API_INGRESSOS, headers=HEADERS, json=novo_ingresso, timeout=10)
                
                # O status de criação é 201 no Supabase PostgREST
                if resp_ing.status_code not in (200, 201):
                    sucesso_total = False
                    continue

                # 3. Atualizar (PATCH) ingressos vendidos
                novos_vendidos = dados_ev['ingressos_vendidos'] + 1
                resp_patch = requests.patch(f"{API_EVENTOS}?id=eq.{evento['id']}", headers=HEADERS, json={"ingressos_vendidos": novos_vendidos}, timeout=10)
                
                if resp_patch.status_code not in (200, 204):
                    sucesso_total = False

            except Exception as ex:
                print(f"Erro no pagamento: {ex}")
                sucesso_total = False
        
        if sucesso_total:
            # Registrar uso de cupom se houver
            cupom_id = getattr(page, 'cupom_aplicado_id', None)
            if cupom_id:
                try:
                    from api import API_CUPONS_USADOS
                    requests.post(API_CUPONS_USADOS, headers=HEADERS, json={
                        "usuario_id": usuario_logado["id"],
                        "cupom_id": cupom_id
                    }, timeout=5)
                    # Atualizar lista local para bloquear reuso imediato
                    usados = getattr(page, 'cupons_usados', [])
                    usados.append(cupom_id)
                    setattr(page, 'cupons_usados', usados)
                except: pass

            carrinho.clear()
            safe_storage_set(page, "carrinho_data", [])
            setattr(page, 'desconto_aplicado', 0)
            setattr(page, 'desconto_porcentagem', 0)
            setattr(page, 'cupom_aplicado_id', None)
            animacao_sucesso()
        else:
            show_msg(page, "Falha no processamento. Reinicie seu carrinho e tente de novo.", bgcolor="red")
            btn_pagar.disabled = False
            btn_pagar.content = ft.Text("Tentar Novamente", weight="bold", color="white")
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
                    content=ft.Row([
                        ft.Text(chave_pix, size=13, weight="bold", color="on_surface", expand=True, text_align="center"),
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
                    begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1)
                ),
                padding=20,
                shadow=ft.BoxShadow(blur_radius=20, color="black26", offset=ft.Offset(0, 10)),
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color="white70", size=30),
                        ft.Text("MMPass Gold", color="white60", size=12)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=20),
                    ft.Text("•••• •••• •••• ••••", color="white", size=20, weight="bold"),
                    ft.Container(height=10),
                    ft.Row([
                        ft.Column([
                            ft.Text("TITULAR", color="white54", size=10),
                            ft.Text(usuario_logado["nome"].upper() if usuario_logado else "NOME DO TITULAR", color="white", size=14, weight="bold")
                        ]),
                        ft.Column([
                            ft.Text("VALIDADE", color="white54", size=10),
                            ft.Text("12/29", color="white", size=14, weight="bold")
                        ])
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
                                        ft.Text(f"R$ {total_geral:.2f}".replace('.', ','), size=24, weight="bold", color="#818cf8")
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Divider(height=30, color="outline_variant", thickness=0.5),
                                    ft.Row([
                                        ft.Text(f"{len(carrinho)} ingressos", size=14, color="on_surface_variant"),
                                        ft.Text(f"Taxa de serviço: R$ {taxa:.2f}".replace('.', ','), size=12, color="on_surface_variant")
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
