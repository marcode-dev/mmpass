"""
Componentes de UI Compartilhados.
Contém barras de navegação (BottomBar/TopBar), animações globais e estilos universais para manter a consistência visual.
"""
import flet as ft

def get_bottom_bar(page, app_view, route):
    return ft.Container(
        height=75,
        bgcolor="surface",
        blur=ft.Blur(20, 20),
        border=ft.border.only(top=ft.border.BorderSide(0.5, "outline_variant")),
        padding=ft.padding.only(bottom=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.HOME_ROUNDED,
                    icon_size=28,
                    selected=True,
                    selected_icon=ft.Icons.HOME_ROUNDED,
                    icon_color="on_surface_variant",
                    selected_icon_color="#818cf8",
                    on_click=lambda e: route(page, app_view, "home"),
                ),
                ft.IconButton(
                    icon=ft.Icons.CONFIRMATION_NUMBER_OUTLINED,
                    icon_size=28,
                    icon_color="on_surface_variant",
                    on_click=lambda e: route(page, app_view, "cupons"),
                ),
                ft.IconButton(
                    icon=ft.Icons.PERSON_OUTLINE_ROUNDED,
                    icon_size=28,
                    icon_color="on_surface_variant",
                    on_click=lambda e: route(page, app_view, "perfil"),
                ),
            ],
        ),
    )

def card_evento(evento, page, app_view, route, largura=250):
    img_url = evento.get("imagem") or evento.get("Imagem") or "https://via.placeholder.com/150"
    is_destaque = largura is not None and largura > 200
    evento_id = evento.get("id")
    
    # Lógica de Favoritos (Resiliente a tipos)
    favoritos = [str(fid) for fid in (getattr(page, 'favoritos', []) or [])]
    ja_favorito = str(evento_id) in favoritos

    def toggle_favorito(e):
        from utils import safe_storage_set
        import requests
        from api import API_FAVORITOS, HEADERS
        import threading
        
        # 1. Obter e Limpar Duplicatas (Safety First)
        raw_favs = getattr(page, 'favoritos', [])
        favs = list(dict.fromkeys(raw_favs)) # Remove duplicatas mantendo ordem
        usuario = getattr(page, 'usuario_logado', None)
        
        if not usuario: return # Não permite favoritar deslogado
        
        if evento_id in favs:
            # Remover
            while evento_id in favs: favs.remove(evento_id)
            e.control.content.icon = ft.Icons.FAVORITE_BORDER_ROUNDED
            e.control.content.color = "white"
            
            def remove_db():
                try: requests.delete(f"{API_FAVORITOS}?usuario_id=eq.{usuario['id']}&evento_id=eq.{evento_id}", headers=HEADERS, timeout=5)
                except: pass
            threading.Thread(target=remove_db).start()
        else:
            # Adicionar
            favs.append(evento_id)
            e.control.content.icon = ft.Icons.FAVORITE_ROUNDED
            e.control.content.color = "#818cf8"
            
            def add_db():
                try: 
                    # Tenta postar, o banco pode aceitar duplicatas mas o código local estará limpo
                    requests.post(API_FAVORITOS, json={"usuario_id": usuario['id'], "evento_id": evento_id}, headers=HEADERS, timeout=5)
                except: pass
            threading.Thread(target=add_db).start()
        
        setattr(page, 'favoritos', favs)
        safe_storage_set(page, "favoritos_data", favs)
        e.control.update()

    return ft.Container(
        width=largura, 
        margin=10,
        padding=0, 
        border_radius=24,
        bgcolor="surface", 
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(
            blur_radius=20, 
            color="black12", 
            offset=ft.Offset(0, 8),
            spread_radius=-2
        ),
        animate=ft.Animation(400, ft.AnimationCurve.DECELERATE),
        on_hover=lambda e: setattr(e.control, "scale", 1.03 if e.data == "true" else 1.0),
        on_click=lambda e: route(page, app_view, "evento", evento=evento),
        content=ft.Column(
            tight=True, 
            spacing=0,
            controls=[
                # Área da Imagem com Gradiente Overlay
                ft.Stack([
                    ft.Image(
                        src=img_url,
                        fit="cover",
                        width=float("inf"),
                        height=160 if is_destaque else 130,
                    ),
                    ft.Container(
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(0, 0.3),
                            end=ft.Alignment(0, 1),
                            colors=["transparent", "black54"]
                        ) if is_destaque else None,
                        expand=True,
                    ),
                    ft.Container(
                        padding=12,
                        top=0, right=0,
                        content=ft.Container(
                            padding=6,
                            bgcolor="white24",
                            blur=10,
                            border_radius=12,
                            on_click=toggle_favorito,
                            content=ft.Icon(
                                ft.Icons.FAVORITE_ROUNDED if ja_favorito else ft.Icons.FAVORITE_BORDER_ROUNDED, 
                                color="#818cf8" if ja_favorito else "white", 
                                size=18
                            )
                        )
                    ) if is_destaque else ft.Container()
                ]),
                # Detalhes
                ft.Container(
                    padding=16,
                    content=ft.Column([
                        ft.Text(
                            evento["nome"], 
                            weight="bold", 
                            size=17 if is_destaque else 15, 
                            color="on_surface",
                            max_lines=1, 
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON_ROUNDED, size=14, color="#818cf8"),
                            ft.Text(evento["local"], size=12, color="on_surface_variant"),
                        ], spacing=4),
                        ft.Container(height=8),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row([
                                    ft.Text("R$ ", size=12, color="#818cf8", weight="bold"),
                                    ft.Text(f'{float(evento["preco"]):.2f}'.replace('.', ','), weight="bold", size=18, color="on_surface"),
                                ], spacing=0),
                                ft.Container(
                                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                    bgcolor="#f1f5f9",
                                    border_radius=8,
                                    content=ft.Text(
                                        evento["data"], 
                                        size=10, 
                                        weight="bold", 
                                        color="on_surface_variant"
                                    )
                                )
                            ]
                        ),
                    ], spacing=4)
                )
            ],
        ),
    )
