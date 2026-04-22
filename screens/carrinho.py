import flet as ft
import requests
from api import API_URL_COMPRAR
from utils import safe_storage_set

def render_carrinho(page, app_view, route):
    carrinho = getattr(page, 'carrinho', None) or []
    cupons_resgatados = getattr(page, 'cupons_resgatados', None) or []
    usuario_logado = getattr(page, 'usuario_logado', None)

    subtotal = sum(float(ev["preco"]) for ev in carrinho)
    taxa_envio = 15.00
    desconto = 0

    texto_desconto = ft.Text("", color="green400", size=14)

    campo_cupom = ft.TextField(
        label="Código de cupom",
        width=220,
        bgcolor="surface_variant",
        border_radius=10,
        filled=True
    )

    texto_total = ft.Text(
        f"R$ {subtotal + taxa_envio:.2f}",
        size=22,
        weight="bold",
        color="orange400"
    )

    def aplicar_cupom(e):
        nonlocal desconto
        codigo = campo_cupom.value.upper()
        if codigo == "MAKO5":
            desconto = 5
        elif codigo == "MAKO10":
            desconto = subtotal * 0.10
        elif codigo == "VIP20":
            desconto = subtotal * 0.20
        elif codigo == "DIAMOND30":
            desconto = subtotal * 0.30
        else:
            desconto = 0
            texto_desconto.value = "❌ Cupom inválido"
            texto_desconto.color = "red400"
            page.update()
            return

        total = subtotal + taxa_envio - desconto
        texto_total.value = f"R$ {total:.2f}"
        texto_desconto.value = f"✅ - R$ {desconto:.2f} aplicado"
        texto_desconto.color = "green400"
        campo_cupom.value = ""
        page.update()

    def remover_item(evento):
        if evento in carrinho:
            carrinho.remove(evento)
            setattr(page, 'carrinho', carrinho)
            # Salvar no armazenamento persistente
            safe_storage_set(page, "carrinho_data", carrinho)
        route(page, app_view, "carrinho")

    def fechar_animacao(dialog):
        dialog.open = False
        page.update()

    def animacao_compra():
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320,
                height=320,
                padding=20,
                border_radius=25,
                bgcolor="white",
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=90),
                        ft.Text("Compra realizada!", size=24, weight=ft.FontWeight.BOLD, color="on_surface"),
                        ft.Text("Seu ingresso foi emitido com sucesso.", text_align="center", color="on_surface_variant"),
                        ft.Container(height=10),
                        ft.Button(
                            "Ver meus ingressos",
                            on_click=lambda e: (fechar_animacao(dialog), route(page, app_view, "ingressos"))
                        )
                    ]
                )
            )
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def sua_funcao_de_pagamento(e, cupom):
        if not usuario_logado:
            page.snack_bar = ft.SnackBar(ft.Text("Atenção: Faça login para finalizar a compra"))
            page.snack_bar.open = True
            page.update()
            return

        if not carrinho:
            page.snack_bar = ft.SnackBar(ft.Text("Carrinho vazio"))
            page.snack_bar.open = True
            page.update()
            return
            
        for evento in carrinho:
            dados = {
                "action": "comprar",
                "usuario_id": usuario_logado["id"],
                "evento_id": evento["id"]
            }
            response = requests.post(API_URL_COMPRAR, json=dados)
            try:
                resultado = response.json()
                if resultado.get("status") != "sucesso":
                    print("Erro ao comprar:", resultado)
            except:
                print("Erro na resposta da API")

        carrinho.clear()
        setattr(page, 'carrinho', carrinho)
        animacao_compra()

    itens = []
    for evento in carrinho:
        card = ft.Container(
            padding=10,
            margin=ft.margin.symmetric(horizontal=15, vertical=5),
            border_radius=15,
            bgcolor="surface",
            shadow=ft.BoxShadow(blur_radius=10, color="black12", offset=ft.Offset(0, 2)),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        expand=True,
                        on_click=lambda e, ev=evento: route(page, app_view, "evento", evento=ev),
                        content=ft.Row([
                            ft.Container(
                                width=60,
                                height=60,
                                border_radius=10,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=ft.Image(
                                    src=evento.get("imagem", ""),
                                    fit="cover",
                                )
                            ),
                            ft.Column(
                                expand=True,
                                spacing=2,
                                controls=[
                                    ft.Text(evento["nome"], weight="bold", size=15, color="on_surface", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(f'R$ {evento["preco"]}', color="#818cf8", weight="bold", size=14),
                                ]
                            ),
                        ], spacing=15)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="red400",
                        icon_size=20,
                        tooltip="Remover",
                        on_click=lambda e, ev=evento: remover_item(ev)
                    )
                ]
            )
        )
        itens.append(card)

    resumo = ft.Container(
        padding=20,
        margin=15,
        border_radius=20,
        bgcolor="surface",
        shadow=ft.BoxShadow(blur_radius=20, color="black12", offset=ft.Offset(0, 5)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Resumo do Pedido", size=20, weight="bold"),
                ft.Row([ft.Text("Subtotal"), ft.Text(f"R$ {subtotal:.2f}")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("Taxa de envio"), ft.Text(f"R$ {taxa_envio:.2f}")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("Desconto"), texto_desconto], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Row([ft.Text("Total Geral", weight="bold"), texto_total], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text("Cupom de desconto", weight="bold"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        campo_cupom,
                        ft.ElevatedButton(
                            "Aplicar",
                            on_click=aplicar_cupom,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor="blue400",
                                color="white"
                            )
                        )
                    ]
                ),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Finalizar Compra",
                    icon=ft.Icons.PAYMENT,
                    width=300,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="purple500",
                        color="white",
                        overlay_color="white24",
                        shape=ft.RoundedRectangleBorder(radius=15)
                    ),
                    on_click=lambda _: route(page, app_view, "pagamento")
                )
            ]
        )
    )

    top_bar_carrinho = ft.Container(
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
                ft.Container(width=10),
                ft.Text("Meu Carrinho", size=26, weight=ft.FontWeight.BOLD, color="on_surface", expand=True),
            ]
        )
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                top_bar_carrinho,
                ft.Divider(color="black12"),
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        *itens,
                        resumo
                    ]
                )
            ]
        )
    )
