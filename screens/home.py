import flet as ft
from shared_ui import get_bottom_bar, card_evento

def render_home(page, app_view, route):
    page.fundo_mestre.gradient = None
    page.fundo_mestre.bgcolor = ft.Colors.WHITE
    page.update()
    app_view.scroll = None
    app_view.expand = True

    eventos_todos = getattr(page, 'eventos', None) or []
    
    # Cálculo Global de Ingressos (Em Alta)
    from api import API_INGRESSOS, HEADERS
    import requests
    ingressos_counts = {}
    try:
        resp = requests.get(f"{API_INGRESSOS}?select=evento_id", headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            ingressos = resp.json()
            for i in ingressos:
                eid = i.get("evento_id")
                if eid:
                    ingressos_counts[eid] = ingressos_counts.get(eid, 0) + 1
    except:
        pass

    # Injeta o contador nos eventos
    for e in eventos_todos:
        e["ingressos_vendidos"] = ingressos_counts.get(e["id"], 0)

    # Filtra Em Alta (Mais de 5 ingressos)
    eventos_em_alta = sorted(
        [e for e in eventos_todos if e["ingressos_vendidos"] > 5],
        key=lambda x: x["ingressos_vendidos"],
        reverse=True
    )
    
    # Regra de exibição: Máximo 5 eventos em exibição
    mostrar_em_alta = len(eventos_em_alta) > 0
    if mostrar_em_alta:
        eventos_em_alta = eventos_em_alta[:5]
    
    # Se não houver eventos, mostra estado de erro com Retry
    if not eventos_todos:
        app_view.controls.append(
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Icon(ft.Icons.CLOUD_OFF, size=50, color="on_surface_variant"),
                    ft.Text("Não conseguimos carregar os eventos.", size=16),
                    ft.ElevatedButton(
                        "Tentar Novamente", 
                        icon=ft.Icons.REFRESH,
                        on_click=lambda _: route(page, app_view, "home") # Recarrega a rota
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )
        return

    # Containers de conteúdo
    carrossel_row = ft.Row(
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[card_evento(e, page, app_view, route, largura=280) for e in eventos_em_alta],
    )

    # --- Lógica de Paginação ---
    itens_por_pág = 10
    total_pags = (len(eventos_todos) + itens_por_pág - 1) // itens_por_pág
    
    def get_eventos_pagina(pagina):
        inicio = (pagina - 1) * itens_por_pág
        fim = inicio + itens_por_pág
        return eventos_todos[inicio:fim]

    # Estado local da página (inicia na 1)
    page_state = {"atual": 1}

    lista_vertical = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    def atualizar_lista(pagina):
        page_state["atual"] = pagina
        evs = get_eventos_pagina(pagina)
        lista_vertical.controls = [card_evento(e, page, app_view, route, largura=None) for e in evs]
        
        # Atualiza controles de paginação
        btn_prev.disabled = (pagina == 1)
        btn_next.disabled = (pagina >= total_pags)
        txt_pag.value = f"Página {pagina} de {total_pags}"
        
        page.update()

    # Controles de Paginação (UI)
    btn_prev = ft.IconButton(
        ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, 
        disabled=True, 
        on_click=lambda _: atualizar_lista(page_state["atual"] - 1),
        icon_size=18, icon_color="#818cf8"
    )
    btn_next = ft.IconButton(
        ft.Icons.ARROW_FORWARD_IOS_ROUNDED, 
        disabled=(total_pags <= 1), 
        on_click=lambda _: atualizar_lista(page_state["atual"] + 1),
        icon_size=18, icon_color="#818cf8"
    )
    txt_pag = ft.Text(f"Página 1 de {total_pags}", size=14, weight="w500", color="on_surface_variant")

    controles_paginacao = ft.Row([
        btn_prev,
        txt_pag,
        btn_next
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20) if total_pags > 1 else ft.Container()

    # Inicializa primeira página
    atualizar_lista(1)

    def filtrar_eventos(texto):
        texto = texto.lower()
        
        # Filtrar Carrossel
        carrossel_row.controls = [
            card_evento(e, page, app_view, route, largura=280) 
            for e in eventos_todos if texto in e["nome"].lower()
        ]
        
        # Filtrar Lista Vertical
        lista_vertical.controls = [
            card_evento(e, page, app_view, route, largura=None) 
            for e in eventos_todos if texto in e["nome"].lower()
        ]
        
        # Mensagem se nada for encontrado
        if not lista_vertical.controls:
            lista_vertical.controls = [
                ft.Container(
                    padding=30,
                    content=ft.Text("Nenhum evento encontrado com esse nome... 🔍", color="on_surface_variant")
                )
            ]
            
        page.update()

    campo_busca = ft.TextField(
        hint_text="Encontre sua próxima experiência...",
        expand=True,
        border_radius=18,
        border_color="transparent",
        filled=True,
        bgcolor="surface",
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        prefix_style=ft.TextStyle(color="#818cf8"),
        color="on_surface",
        on_change=lambda e: filtrar_eventos(e.control.value)
    )

    header = ft.Container(
        padding=ft.Padding(15, 20, 15, 10),
        gradient=ft.LinearGradient(
            colors=["#87e4e7", "#ebb1d4"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        border_radius=ft.BorderRadius(bottom_left=24, bottom_right=24, top_left=0, top_right=0),
        content=ft.Row([
            campo_busca,
            ft.Container(
                bgcolor="white24",
                border_radius=12,
                padding=2,
                content=ft.IconButton(
                    icon=ft.Icons.SHOPPING_CART_OUTLINED,
                    icon_color="white",
                    icon_size=24,
                    on_click=lambda e: route(page, app_view, "carrinho")
                )
            )
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    bottom_bar = get_bottom_bar(page, app_view, route)

    # Montar controles do scroll dinamicamente
    main_scroll_controls = [header]
    if mostrar_em_alta:
        main_scroll_controls.extend([
            ft.Container(
                padding=ft.Padding(20, 25, 0, 5),
                content=ft.Row([
                    ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color="#818cf8", size=24),
                    ft.Text("Em Alta", size=20, weight="bold", color="on_surface")
                ], spacing=8),
            ),
            ft.Container(
                margin=ft.Margin(10, 0, 0, 0),
                content=carrossel_row
            ),
        ])

    main_scroll_controls.extend([
        ft.Container(
            padding=ft.Padding(20, 20, 0, 5),
            content=ft.Row([
                ft.Icon(ft.Icons.EXPLORE_ROUNDED, color="#818cf8", size=24),
                ft.Text("Explorar Todos", size=20, weight="bold", color="on_surface")
            ], spacing=8),
        ),
        ft.Container(
            padding=ft.Padding(10, 0, 10, 0),
            content=lista_vertical
        ),
        ft.Container(
            padding=ft.Padding(0, 20, 0, 20),
            content=controles_paginacao
        ),
        ft.Container(height=100)
    ])

    scroll_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=main_scroll_controls
    )

    app_view.controls.append(scroll_content)
    app_view.controls.append(bottom_bar)