"""
Tela de Meus Ingressos.
Realiza junção no Supabase (eventos + ingressos) e gera o QR Code visual para entrada na festa.
"""
import flet as ft
import requests
from api import API_INGRESSOS, HEADERS
from utils import gerar_qr

def render_ingressos(page, app_view, route):
    usuario_logado = getattr(page, 'usuario_logado', None)
    
    if usuario_logado is None:
        page.snack_bar = ft.SnackBar(ft.Text("Faça login primeiro"))
        page.snack_bar.open = True
        page.update()
        return

    try:
        # Busca no Supabase puxando dados da tabela relacional "eventos" e o campo "desconto"
        url = f"{API_INGRESSOS}?usuario_id=eq.{usuario_logado['id']}&select=id,data_compra,desconto,codigo,eventos(*)"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            raw_ingressos = response.json()
            # Mapeamos para o formato antigo para não quebrar a UI
            ingressos = []
            for item in raw_ingressos:
                if item.get("eventos"):
                    ev = item["eventos"]
                    cupom_id = item.get("desconto")
                    lista_cupons = getattr(page, 'lista_cupons', [])
                    cupom_info = next((c for c in lista_cupons if c["id"] == cupom_id), None)
                    porcentagem = int(cupom_info["desconto%"]) if cupom_info else 0

                    ingressos.append({
                        "ingresso_id": item["id"],
                        "codigo": item.get("codigo"),
                        "nome": ev["nome"],
                        "data": ev["data"],
                        "local": ev["local"],
                        "imagem": ev.get("imagem"),
                        "desconto_perc": porcentagem,
                        "cupom_id": cupom_id
                    })
        else:
            ingressos = []
    except Exception as e:
        print(f"Erro ao buscar ingressos: {e}")
        ingressos = []

    # 1. Ordenação por data do evento
    from datetime import datetime
    
    def parse_date(date_str):
        try:
            # Tenta converter DD/MM/YYYY para objeto datetime para ordenação
            return datetime.strptime(date_str, "%d/%m/%Y")
        except:
            try:
                # Tenta formato ISO se falhar
                return datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")
            except:
                return datetime.max

    ingressos.sort(key=lambda x: parse_date(x['data']))

    def abrir_modal_ingresso(ingresso):
        qr = gerar_qr(ingresso['codigo'])
        
        def fechar_dialog(e):
            modal.open = False
            page.update()

        modal = ft.AlertDialog(
            content=ft.Container(
                width=350,
                height=500, # Altura fixa para garantir o scroll na versão atual
                padding=10,
                bgcolor="surface",
                border_radius=20,
                content=ft.Column([
                    ft.Container(
                        padding=15, bgcolor="purple50", border_radius=50,
                        content=ft.Icon(ft.Icons.LOCAL_ACTIVITY, size=40, color="purple600")
                    ),
                    ft.Column([
                        ft.Text(ingresso["nome"].upper(), size=22, weight="bold", color="on_surface", text_align="center"),
                        ft.Text(f"ID: #{ingresso['ingresso_id']}", size=12, color="on_surface_variant"),
                        ft.Row([
                            ft.Container(
                                visible=bool(ingresso.get("desconto_perc")),
                                padding=ft.Padding(8, 4, 8, 4),
                                bgcolor="green50",
                                border_radius=8,
                                content=ft.Text(f"Desconto aplicado: {ingresso.get('desconto_perc')}%", size=11, color="green700", weight="bold")
                            ) if ingresso.get("desconto_perc") else ft.Container(),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    
                    ft.Divider(height=30, color="outline_variant"),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color="purple600"),
                        ft.Text(f"{ingresso['data']}", size=15, weight="w500"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, size=18, color="purple600"),
                        ft.Text(f"{ingresso['local']}", size=14, color="on_surface_variant"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Container(height=15),
                    
                    # Área do QR Code
                    ft.Container(
                        padding=15,
                        bgcolor="white",
                        border_radius=20,
                        border=ft.border.all(1, "outline_variant"),
                        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
                        content=ft.Image(src=qr, width=220, height=220)
                    ),
                    
                    ft.Container(height=15),
                    
                    ft.ElevatedButton(
                        "Fechar", 
                        on_click=fechar_dialog,
                        width=float("inf"), 
                        height=50,
                        bgcolor="purple600", 
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                    )
                ], tight=False, # Alterado para permitir scroll se necessário
                   scroll=ft.ScrollMode.AUTO, 
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                   spacing=10
                )
            )
        )
        page.overlay.append(modal)
        modal.open = True
        page.update()

    lista_cards = []

    if not ingressos:
        lista_cards.append(
            ft.Container(
                content=ft.Text("Você ainda não possui ingressos.", size=18, color="on_surface_variant"),
                margin=ft.Margin(0, 50, 0, 0),
                alignment=ft.Alignment(0, 0) 
            )
        )

    for ingresso in ingressos:
        card = ft.Container(
            margin=ft.Margin(20, 8, 20, 8),
            padding=20, 
            border_radius=20,
            bgcolor="surface",
            border=ft.border.all(1, "outline_variant"),
            on_click=lambda e, i=ingresso: abrir_modal_ingresso(i),
            shadow=ft.BoxShadow(blur_radius=10, color="black12", offset=ft.Offset(0, 4)),
            content=ft.Row([
                # Miniatura/Ícone representativo
                ft.Container(
                    width=60, height=60,
                    bgcolor="grey100",
                    border_radius=15,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Image(
                        src=ingresso.get("imagem") or "https://via.placeholder.com/60",
                        fit="cover",
                    )
                ),
                ft.Container(width=10),
                ft.Column([
                    ft.Text(ingresso["nome"], size=16, weight="bold", color="on_surface", no_wrap=True),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, size=14, color="on_surface_variant"),
                        ft.Text(f"{ingresso['data']}", size=12, color="on_surface_variant"),
                        ft.Container(
                            visible=bool(ingresso.get("desconto_perc")),
                            padding=ft.Padding(6, 2, 6, 2),
                            bgcolor="green50",
                            border_radius=5,
                            content=ft.Text(f"-{ingresso.get('desconto_perc')}%", size=10, color="green700", weight="bold")
                        ) if ingresso.get("desconto_perc") else ft.Container(),
                    ], spacing=5),
                ], expand=True),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=16, color="outline_variant")
            ])
        )
        lista_cards.append(card)

    top_bar_ingressos = ft.Container(
        padding=15, 
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    bgcolor="surface",
                    border_radius=30,
                    shadow=ft.BoxShadow(blur_radius=10, color="black12"),
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="on_surface",
                        on_click=lambda e: route(page, app_view, "perfil")
                    )
                ),
                ft.Text("Meus Ingressos", size=24, weight=ft.FontWeight.BOLD, color="on_surface"),
                ft.IconButton(icon=ft.Icons.HISTORY_ROUNDED, icon_color="on_surface"),
            ]
        )
    )

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                top_bar_ingressos,
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=lista_cards
                )
            ]
        )
    )
