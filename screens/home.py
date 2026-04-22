"""
Tela Principal (Home).
Lista eventos em destaque, sistema de busca iterativo e filtragem de categorias de festas consultando do Supabase.
"""
import flet as ft
from shared_ui import get_bottom_bar, card_evento

def render_home(page, app_view, route):
    app_view.scroll = None
    app_view.expand = True

    eventos_todos = getattr(page, 'eventos', None) or []
    
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
        controls=[card_evento(e, page, app_view, route, largura=280) for e in eventos_todos],
    )

    lista_vertical = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
        controls=[card_evento(e, page, app_view, route, largura=None) for e in eventos_todos],
    )

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
        padding=ft.padding.only(top=50, left=15, right=15, bottom=25),
        gradient=ft.LinearGradient(
            colors=["#93c5fd", "#818cf8"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        border_radius=ft.BorderRadius(bottom_left=30, bottom_right=30, top_left=0, top_right=0),
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

    scroll_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[
            header,
            ft.Container(
                padding=ft.padding.only(left=20, bottom=5, top=25),
                content=ft.Row([
                    ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color="#818cf8", size=24),
                    ft.Text("Em Alta", size=20, weight="bold", color="on_surface")
                ], spacing=8),
            ),
            ft.Container(
                margin=ft.margin.only(left=10),
                content=carrossel_row
            ),
            ft.Container(
                padding=ft.padding.only(left=20, top=20, bottom=5),
                content=ft.Row([
                    ft.Icon(ft.Icons.EXPLORE_ROUNDED, color="#818cf8", size=24),
                    ft.Text("Sugestões para você", size=20, weight="bold", color="on_surface")
                ], spacing=8),
            ),
            ft.Container(
                padding=ft.padding.only(left=10, right=10),
                content=lista_vertical
            ),
            ft.Container(height=100)
        ]
    )

    app_view.controls.append(scroll_content)
    app_view.controls.append(bottom_bar)
