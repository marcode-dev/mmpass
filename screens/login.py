"""
Tela de Login.
Autentica informações do usuário através do Supabase e valida a chave local através de bcrypt.
"""
import flet as ft
import requests
import bcrypt
from api import API_USUARIOS, HEADERS
from chat import update_chat_visibility
from utils import show_msg, safe_storage_set

def render_login(page, app_view, route):
    # Inputs com estilo moderno
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
        hint_text="••••••••",
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

    def fazer_login(e):
        if not email.value or not senha.value:
            mensagem.value = "Preencha todos os campos"
            page.update()
            return

        btn_entrar.disabled = True
        btn_entrar.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
        page.update()

        try:
            # Buscando o usuário pelo email
            url = f"{API_USUARIOS}?email=eq.{email.value}"
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                usuarios = response.json()
             
                if len(usuarios) > 0:
                    usuario = usuarios[0]
                    hash_banco = usuario.get("senha", "")
                    
                    # Verificando o hash com a bcrypt
                    senha_digitada = senha.value.encode('utf-8')
                    if hash_banco and bcrypt.checkpw(senha_digitada, hash_banco.encode('utf-8')):
                        safe_storage_set(page, "usuario_logado", usuario)
                        setattr(page, 'usuario_logado', usuario)
                        
                        # Sincronização imediata pós-login
                        from utils import sync_user_data
                        sync_user_data(page)
                        
                        show_msg(page, f"Bem-vindo de volta, {usuario['nome']}! 👋")
                        update_chat_visibility(page)
                        route(page, app_view, "home")
                        return
                    else:
                        mensagem.value = "Senha incorreta"
                else:
                    mensagem.value = "Usuário não encontrado"
            else:
                 mensagem.value = f"Erro na API: {response.text}"
        except Exception as ex:
            mensagem.value = "Erro de conexão com o servidor"
            print(ex)
        
        btn_entrar.disabled = False
        btn_entrar.content = ft.Text("Entrar", weight="bold", color="white")
        page.update()

    btn_entrar = ft.Container(
        content=ft.Text("Entrar", weight="bold", color="white"),
        alignment=ft.Alignment(0, 0),
        width=320,
        height=55,
        bgcolor="#818cf8",
        border_radius=18,
        on_click=fazer_login,
        shadow=ft.BoxShadow(blur_radius=15, color="purple200", offset=ft.Offset(0, 5))
    )

    card_login = ft.Container(
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
                    ft.Text("Sua próxima experiência começa aqui.", size=14, color="on_surface_variant", text_align="center"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                
                ft.Column([
                    email,
                    senha,
                    mensagem,
                ], spacing=15),
                
                ft.Column([
                    btn_entrar,
                    ft.Row([
                        ft.Text("Não tem conta?", size=13, color="on_surface_variant"),
                        ft.TextButton(
                            "Criar Agora", 
                            style=ft.ButtonStyle(color="#818cf8"),
                            on_click=lambda e: route(page, app_view, "cadastro")
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
                    content=card_login
                )
            ])
        )
    )
