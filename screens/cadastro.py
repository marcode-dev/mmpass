import flet as ft
import requests
from api import CADASTRO_API

def render_cadastro(page, app_view, route):
    nome = ft.TextField(label="Nome", width=320, filled=True, bgcolor="surface_variant")
    email = ft.TextField(label="Email", width=320, filled=True, bgcolor="surface_variant")
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=320, filled=True, bgcolor="surface_variant")
    mensagem = ft.Text("", color="red")

    def cadastrar(e):
        dados = {"nome": nome.value, "email": email.value, "senha": senha.value}
        try:
            response = requests.post(CADASTRO_API, json=dados)
            resultado = response.json()
            if resultado.get("status") == "sucesso":
                mensagem.value = "Conta criada com sucesso!"
                mensagem.color = "green"
            else:
                mensagem.value = "Erro ao cadastrar"
        except:
            mensagem.value = "Erro no servidor"
        page.update()

    card = ft.Container(
        width=360,
        padding=30,
        border_radius=20,
        bgcolor="surface",
        shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK12),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            spacing=15,
            controls=[
                ft.Container(
                    content=ft.Image(src="logo.png", width=100),
                    bgcolor="#1e293b",
                    padding=15,
                    border_radius=15,
                    margin=ft.margin.only(bottom=5),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK26)
                ),
                ft.Text("Criar Conta", size=28, weight=ft.FontWeight.BOLD, color="on_surface"),
                nome, email, senha, mensagem,
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
                        "Cadastrar",
                        color="white",
                        bgcolor="transparent",
                        elevation=0,
                        on_click=cadastrar
                    )
                ),
                ft.TextButton("Voltar ao login", on_click=lambda e: route(page, app_view, "login"))
            ]
        )
    )

    app_view.controls.append(
        ft.Container(
            content=card,
            expand=True,          
            alignment=ft.Alignment(0, 0), 
        )
    )
