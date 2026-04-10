import flet as ft
from shared_ui import get_bottom_bar
from chat import update_chat_visibility

def render_perfil(page, app_view, route):
    usuario_logado = getattr(page, 'usuario_logado', None)
    
    if usuario_logado is None:
        route(page, app_view, "login")
        return

    def logout(e):
        setattr(page, 'usuario_logado', None)
        setattr(page, 'carrinho', [])
        setattr(page, 'cupons_resgatados', [])
        update_chat_visibility(page)
        route(page, app_view, "login")

    def abrir_configuracoes(e):
        def mudar_tema(e):
            page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            dialog.open = False
            page.update()

        def fechar_dialogo(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Configurações"),
            content=ft.Column(
                [
                    ft.Button("Alternar tema", icon=ft.Icons.BRIGHTNESS_4, on_click=mudar_tema),
                    ft.TextButton("Fechar", on_click=fechar_dialogo)
                ],
                tight=True,
            ),
        )
        page.overlay.append(dialog) 
        dialog.open = True
        page.update()

    header = ft.Container(
        padding=ft.padding.only(top=40, bottom=40),
        gradient=ft.LinearGradient(
            colors=["#93c5fd", "#818cf8"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        width=float("inf"),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.PURPLE_200, offset=ft.Offset(0, 5)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.CircleAvatar(
                    radius=55,
                    bgcolor="white",
                    content=ft.Text(
                        usuario_logado["nome"][0].upper(),
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        color="#818cf8"
                    ),
                ),
                ft.Container(height=10),
                ft.Text(usuario_logado["nome"], size=26, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(usuario_logado["email"], color="white70"),
            ]
        )
    )

    perfil_conteudo = ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[
            header,
            ft.Container(height=30),
            ft.Container(
                width=320,
                padding=20,
                border_radius=20,
                bgcolor="white",
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CONFIRMATION_NUMBER),
                            title=ft.Text("Meus Ingressos"),
                            on_click=lambda e: route(page, app_view, "ingressos")
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.FAVORITE),
                            title=ft.Text("Eventos Favoritos"),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS),
                            title=ft.Text("Configurações"),
                            on_click=abrir_configuracoes 
                        ),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOGOUT),
                            title=ft.Text("Sair"),
                            on_click=logout
                        ),
                    ],
                )
            ),
        ]
    )

    bottom_bar = get_bottom_bar(page, app_view, route)

    app_view.controls.append(
        ft.Column(
            expand=True,
            controls=[
                perfil_conteudo,
                bottom_bar
            ]
        )
    )
