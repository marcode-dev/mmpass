import flet as ft

def route(page: ft.Page, app_view: ft.Column, route_name: str, **kwargs):
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
    elif route_name == "ingressos":
        from screens.ingressos import render_ingressos
        render_ingressos(page, app_view, route)
        
    page.update()
