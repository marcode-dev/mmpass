import flet as ft
import requests
from api import LOGIN_API
from chat import update_chat_visibility

def render_login(page, app_view, route):
    email = ft.TextField(label="Email", width=320, border_radius=12, filled=True, bgcolor="white")
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=320, border_radius=12, filled=True, bgcolor="white")
    mensagem = ft.Text("", color="red")

    def fazer_login(e):
        dados = {"email": email.value, "senha": senha.value}
        try:
            response = requests.post(LOGIN_API, json=dados)
            resultado = response.json()
            if resultado.get("status") == "sucesso":
                setattr(page, 'usuario_logado', resultado["usuario"])
                update_chat_visibility(page)
                route(page, app_view, "home")
            else:
                mensagem.value = f"Email ou senha inválidos"
        except Exception as ex:
            mensagem.value = "Erro ao conectar com servidor"
        page.update()

    card_login = ft.Container(
        width=360,
        padding=30,
        border_radius=20,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=25, spread_radius=1, color=ft.Colors.BLACK26),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            spacing=15,
            controls=[
                ft.Text("MMPass", size=32, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Compre ingressos em segundos", size=14, color="grey"),
                email,
                senha,
                mensagem,
                ft.Container(
                    width=320,
                    height=50,
                    border_radius=25,
                    gradient=ft.LinearGradient(
                        colors=["#93c5fd", "#818cf8"],
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                    ),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.PURPLE_200, offset=ft.Offset(0, 5)),
                    content=ft.ElevatedButton(
                        "Entrar",
                        color="white",
                        bgcolor="transparent",
                        elevation=0,
                        on_click=fazer_login
                    )
                ),
                ft.TextButton("Criar nova conta", on_click=lambda e: route(page, app_view, "cadastro"))
            ]
        )
    )

    app_view.controls.append(
        ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Image(src="logo.png", width=150),
                    card_login
                ]
            )
        )
    )
