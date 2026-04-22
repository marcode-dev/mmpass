import flet as ft
import traceback

def route(page: ft.Page, app_view: ft.Column, route_name: str, **kwargs):
    try:
        app_view.controls.clear()
        app_view.scroll = None
        
        if route_name == "login":
            from screens.login import render_login
            render_login(page, app_view, route)
        elif route_name == "cadastro":
            from screens.cadastro import render_cadastro
            render_cadastro(page, app_view, route)
        elif route_name == "home":
            from screens.home import render_home
            render_home(page, app_view, route)
        elif route_name == "evento":
            from screens.evento import render_evento
            render_evento(page, app_view, route, kwargs.get("evento"))
        elif route_name == "perfil":
            from screens.perfil import render_perfil
            render_perfil(page, app_view, route)
        elif route_name == "cupons":
            from screens.cupons import render_cupons
            render_cupons(page, app_view, route)
        elif route_name == "carrinho":
            from screens.carrinho import render_carrinho
            render_carrinho(page, app_view, route)
        elif route_name == "pagamento":
            from screens.pagamento import render_pagamento
            render_pagamento(page, app_view, route)
        elif route_name == "ingressos":
            from screens.ingressos import render_ingressos
            render_ingressos(page, app_view, route)
        elif route_name == "favoritos":
            from screens.favoritos import render_favoritos
            render_favoritos(page, app_view, route)
            
        page.update()
    except Exception as e:
        # Se houver erro, exibe na tela para diagnóstico rápido
        error_msg = traceback.format_exc()
        app_view.controls.clear()
        app_view.controls.append(
            ft.Container(
                padding=20,
                bgcolor="red100",
                border_radius=10,
                content=ft.Column([
                    ft.Text("Erro durante a navegação:", color="red", weight="bold"),
                    ft.Text(error_msg, color="black", size=12, selectable=True)
                ], scroll=ft.ScrollMode.AUTO)
            )
        )
        page.update()
