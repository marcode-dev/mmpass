import flet as ft
import requests
import bcrypt
from api import API_USUARIOS, HEADERS

def render_cadastro(page, app_view, route):
    # Inputs com estilo moderno
    nome = ft.TextField(
        label="Nome Completo",
        hint_text="Seu nome",
        border_radius=15,
        border_color="transparent",
        filled=True,
        bgcolor="surface",
        prefix_icon=ft.Icons.PERSON_OUTLINED,
        color="on_surface",
        width=320,
    )
    
    email = ft.TextField(
        label="Email",
        hint_text="seu@email.com",
        border_radius=15,
        border_color="transparent",
        filled=True,
        bgcolor="surface",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        color="on_surface",
        width=320,
    )
    
    senha = ft.TextField(
        label="Senha",
        hint_text="Mínimo 6 caracteres",
        password=True,
        can_reveal_password=True,
        border_radius=15,
        border_color="transparent",
        filled=True,
        bgcolor="surface",
        prefix_icon=ft.Icons.LOCK_OUTLINED,
        color="on_surface",
        width=320,
    )
    
    mensagem = ft.Text("", color="red", size=12)

    def cadastrar(e):
        from utils import show_msg
        
        if not nome.value or not email.value or not senha.value:
            mensagem.value = "Preencha todos os campos"
            page.update()
            return

        # Hash da senha usando bcrypt (encoding para bytes, dps decodando pra string pra salvar)
        senha_hash = bcrypt.hashpw(senha.value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        dados = {
            "nome": nome.value, 
            "email": email.value, 
            "senha": senha_hash
        }
        
        btn_cadastrar.disabled = True
        btn_cadastrar.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
        page.update()

        try:
            # Para Supabase (PostgREST), uma chamada POST insere os dados
            # E Prefer: return=representation nos devolve a row inserida
            response = requests.post(API_USUARIOS, headers=HEADERS, json=dados, timeout=10)
            
            if response.status_code in (200, 201):
                show_msg(page, "Conta criada! 🎉 Faça login agora.", bgcolor="green600")
                route(page, app_view, "login")
                return
            else:
                erro_json = response.json()
                # O Supabase retorna detalhes no campo 'message' ou 'details'
                mensagem.value = f"Erro: {erro_json.get('message', 'Erro ao criar conta no banco')}"
        except Exception as ex:
            mensagem.value = f"Erro de conexão com o servidor"
            print(ex)
        
        btn_cadastrar.disabled = False
        btn_cadastrar.content = ft.Text("Criar Conta", weight="bold", color="white")
        page.update()

    btn_cadastrar = ft.Container(
        content=ft.Text("Criar Conta", weight="bold", color="white"),
        alignment=ft.Alignment(0, 0),
        width=320,
        height=55,
        bgcolor="#818cf8",
        border_radius=18,
        on_click=cadastrar,
        shadow=ft.BoxShadow(blur_radius=15, color="purple200", offset=ft.Offset(0, 5))
    )

    card_cadastro = ft.Container(
        padding=40,
        border_radius=30,
        bgcolor=ft.Colors.with_opacity(0.8, "surface"),
        blur=10,
        width=380,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            spacing=25,
            controls=[
                ft.Column([
                    ft.Text("MMPass", size=42, weight="bold", color="#1e293b"),
                    ft.Text("Faça parte da nossa comunidade.", size=14, color="on_surface_variant", text_align="center"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                
                ft.Column([
                    nome,
                    email,
                    senha,
                    mensagem,
                ], spacing=15),
                
                ft.Column([
                    btn_cadastrar,
                    ft.Row([
                        ft.Text("Já possui conta?", size=13, color="on_surface_variant"),
                        ft.TextButton(
                            "Fazer Login", 
                            style=ft.ButtonStyle(color="#818cf8"),
                            on_click=lambda e: route(page, app_view, "login")
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=10)
            ]
        )
    )

    app_view.controls.append(
        ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                colors=["#93c5fd", "#818cf8", "#c7d2fe"],
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
            ),
            content=ft.Stack([
                # Decorativos de fundo
                ft.Container(width=200, height=200, bgcolor="white24", border_radius=100, top=-50, left=-50, blur=50),
                ft.Container(width=150, height=150, bgcolor="white24", border_radius=75, bottom=-30, right=-30, blur=40),
                # Card Central
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=card_cadastro
                )
            ])
        )
    )
