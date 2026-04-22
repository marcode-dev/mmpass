import flet as ft
import requests
import random
import qrcode
import base64
from io import BytesIO

API_URL = "http://127.0.0.1/appstore_wallet/index.php?action=eventos&rand="+str(random.randint(1, 2000))
API_URL_COMPRAR = "http://127.0.0.1/appstore_wallet/index.php?action=comprar"
API_MEUS_INGRESSOS = "http://127.0.0.1/appstore_wallet/index.php?action=meus_ingressos"
LOGIN_API = "http://127.0.0.1/appstore_wallet/login.php"
CADASTRO_API = "http://127.0.0.1/appstore_wallet/cadastro.php"

def main(page: ft.Page):
    page.title = "MMPass"
    page.padding = 0
    page.spacing = 0
    page.window_full_screen = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.assets_dir = "assets"
    

    fundo_mestre = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            colors=['#8fd3f4', "#c471ed"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
    )

    app_view = ft.Column(
        expand=True,
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        width=float("inf"),
    )

    fundo_mestre.content = app_view
    page.add(fundo_mestre)

    eventos = requests.get(API_URL).json()

    usuario_logado = None
    carrinho = []
    def obter_total_ingressos():
        try:
            response = requests.get(
                f"{API_MEUS_INGRESSOS}&usuario_id={usuario_logado['id']}"
            )
            dados = response.json()
            return len(dados)
        except:
            return 0
    cupons_resgatados = [] 
    
    #  CHAT FLUTUANTE
    
    def atualizar_chat():
        if usuario_logado:
            botao_chat.visible = True
            chat_box.visible = False
        else:
            botao_chat.visible = False
            chat_box.visible = False

        page.update()

    chat_aberto = False

    chat_mensagens = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=8,
        auto_scroll=True
    )

    chat_mensagens.controls.append(
        ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    bgcolor="#EEEEEE",
                    padding=10,
                    border_radius=15,
                    width=220,
                    content=ft.Text(
                        "Oi 😄 sou sua assistente! Como posso ajudar?",
                        color="black",
                        no_wrap=False
                    )
                )
            ]
        )
    )

    campo_msg = ft.TextField(
        hint_text="Digite sua mensagem...",
        expand=True,
        border_radius=20,
        filled=True,
        bgcolor="#f1f1f1",
        border_color="transparent"
    )

    # RESPOSTA DO BOT
    def responder_chat(msg):

        if "evento" in msg:
            resposta = "Tem vários eventos disponíveis 🎟️ Dá uma olhada na tela inicial!"

        elif "ola" in msg:
            resposta = "Olá, sou sua Assistente Virtual, tire suas dúvidas aqui!"   

        elif "oi" in msg:
            resposta = "Seja Bem-Vindo ao MMPass, estou aqui para te ajudar!"     

        elif "ingresso" in msg:
            resposta = "Você pode ver seus ingressos na aba de perfil 👤"

        elif "carrinho" in msg:
            pagina_carrinho()
            resposta = "Te levei pro carrinho 🛒"

        elif "cupom" in msg:
            resposta = "Tenta esses: MAKO10, VIP20 ou DIAMOND30 💸"

        elif "valores" in msg:
            resposta = "Você pode conferir os valores na página de cada evento!"

        else:
            resposta = "Entre em contato com a nossa equipe!"

        chat_mensagens.controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        bgcolor="#EEEEEE",
                        padding=10,
                        border_radius=15,
                        width=220,
                        content=ft.Text(resposta, color="black", no_wrap=False)
                    )
                ]
            )
        )

        chat_mensagens.update()


    # ENVIO DO USUÁRIO
    def enviar_mensagem(e):
        if campo_msg.value.strip() == "":
            return

        texto = campo_msg.value

        chat_mensagens.controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.Container(
                        bgcolor="#DCF8C6",
                        padding=10,
                        border_radius=15,
                        width=220,
                        content=ft.Text(texto, color="black", no_wrap=False)
                    )
                ]
            )
        )

        responder_chat(texto.lower())

        campo_msg.value = ""
        page.update()


    
    def toggle_chat(e):
        if usuario_logado is None:
            return

        nonlocal chat_aberto
        chat_aberto = not chat_aberto
        chat_box.visible = chat_aberto
        notificacao.visible = False
        page.update()


    
    chat_box = ft.Container(
        right=20,
        bottom=90,
        width=320,
        height=420,
        border_radius=25,
        visible=False,
        shadow=ft.BoxShadow(blur_radius=25, color="black26"),

        content=ft.Column(
            spacing=0,
            controls=[

                
                ft.Container(
                    padding=15,
                    border_radius=ft.BorderRadius.only(top_left=25, top_right=25),
                    gradient=ft.LinearGradient(colors=["#a855f7", "#7c3aed"]),
                    content=ft.Row(
                        controls=[
                            ft.Text("🧜‍♀️", size=30),
                            ft.Text("Assistente MMPass", color="white", weight="bold")
                        ]
                    )
                ),

               
                ft.Container(
                    height=260,  
                    bgcolor="#f5f5f5",
                    padding=10,
                    content=chat_mensagens
                ),

               
                ft.Container(
                    padding=10,
                    bgcolor="white",
                    border_radius=ft.BorderRadius.only(bottom_left=25, bottom_right=25),
                    content=ft.Row(
                        controls=[
                            campo_msg,
                            ft.Container(
                                bgcolor="#7c3aed",
                                border_radius=20,
                                content=ft.IconButton(
                                    icon=ft.Icons.SEND,
                                    icon_color="white",
                                    on_click=enviar_mensagem
                                )
                            )
                        ]
                    )
                )
            ]
        )
    )

    
    notificacao = ft.Container(
        width=10,
        height=10,
        bgcolor="red",
        border_radius=10,
        right=5,
        top=5,
        visible=True
    )

    
    botao_chat = ft.Container(
        right=20,
        bottom=60,
        content=ft.Stack(
            controls=[
                ft.Container(
                    padding=2,
                    border_radius=50,
                    gradient=ft.LinearGradient(colors=["#a855f7", "#7c3aed"]),
                    shadow=ft.BoxShadow(blur_radius=15, color="purple200"),
                    content=ft.FloatingActionButton(
                        content=ft.Text("🧜‍♀️", size=30),
                        bgcolor="transparent",
                        elevation=0,
                        on_click=toggle_chat
                    )
                ),
                notificacao
            ]
        )
    )

    page.overlay.append(chat_box)
    page.overlay.append(botao_chat)

    atualizar_chat()

    # LOGOUT
    def logout(e):

        nonlocal usuario_logado
        nonlocal carrinho

        usuario_logado = None
        carrinho = []
        

        app_view.controls.clear()
        
        atualizar_chat()

        pagina_login()

        page.update()

    # LOGIN
    def pagina_login():

        app_view.controls.clear()

        email = ft.TextField(
            label="Email",
            width=320,
            border_radius=12,
            filled=True,
            bgcolor="white"
        )

        senha = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=320,
            border_radius=12,
            filled=True,
            bgcolor="white"
        )

        mensagem = ft.Text("", color="red")

        def fazer_login(e):

            nonlocal usuario_logado

            dados = {
                "email": email.value,
                "senha": senha.value
            }

            try:

                response = requests.post(LOGIN_API, json=dados)

                resultado = response.json()

                if resultado["status"] == "sucesso":

                    usuario_logado = resultado["usuario"]
                    
                    atualizar_chat()

                    pagina_home()

                else:

                    mensagem.value = f"Email ou senha inválidos"

            except:

                mensagem.value = "Erro ao conectar com servidor"

            page.update()

        card_login = ft.Container(
            width=360,
            padding=30,
            border_radius=20,
            bgcolor="white",
            shadow=ft.BoxShadow(
                blur_radius=25,
                spread_radius=1,
                color="black26"
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=15,
                controls=[

                    ft.Text(
                        "MMPass",
                        size=32,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        "Compre ingressos em segundos",
                        size=14,
                        color="grey"
                    ),

                    email,
                    senha,

                    mensagem,

                    ft.Button(
                        "Entrar",
                        width=320,
                        height=45,
                        on_click=fazer_login
                    ),

                    ft.TextButton(
                        "Criar nova conta",
                        on_click=lambda e: pagina_cadastro()
                    )
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
                        ft.Image(
                            src="logo.png",
                            width=150
                        ),
                        card_login
                ]
            )
        )
    )

        page.update()
        
            
    # CADASTRO
    
    def pagina_cadastro():

        app_view.controls.clear()

        nome = ft.TextField(
            label="Nome",
            width=320,
            filled=True,
            bgcolor="white"
        )

        email = ft.TextField(
            label="Email",
            width=320,
            filled=True,
            bgcolor="white"
        )

        senha = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=320,
            filled=True,
            bgcolor="white"
        )

        mensagem = ft.Text("", color="red")

        def cadastrar(e):

            dados = {
                "nome": nome.value,
                "email": email.value,
                "senha": senha.value
            }

            try:

                response = requests.post(
                    CADASTRO_API,
                    json=dados
                )

                resultado = response.json()

                if resultado["status"] == "sucesso":

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
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=25, color="black12"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=15,
                controls=[

                    ft.Text(
                        "Criar Conta",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),

                    nome,
                    email,
                    senha,

                    mensagem,

                    ft.Button(
                        "Cadastrar",
                        width=320,
                        height=45,
                        on_click=cadastrar
                    ),

                    ft.Button(
                        "Voltar ao login",
                        on_click=lambda e: pagina_login()
                    )
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

        page.update()

    # LOTAÇÃO
    def cor_lotacao(percentual):
        p = float(percentual)
        if p < 50:
            return "green"
        elif p < 80:
            return "orange"
        else:
            return "red"

    # CLIMA
    def clima_evento():
        opcoes = [
            "☀️ Ensolarado - 27°C",
            "⛅ Parcialmente nublado - 23°C",
            "🌧 Possibilidade de chuva - 20°C",
            "🌙 Noite agradável - 18°C",
        ]
        return random.choice(opcoes)
    
    def adicionar_carrinho(evento):

        carrinho.append(evento)

        page.snack_bar = ft.SnackBar(
            ft.Text("Ingresso adicionado ao carrinho 🛒")
        )

        page.snack_bar.open = True

        pagina_carrinho()

        page.update()
        
    def remover_item(evento):
        if evento in carrinho:
            carrinho.remove(evento)
        pagina_carrinho()

    # PÁGINA EVENTO
    def pagina_evento(evento):

            app_view.controls.clear()

            lotacao_percent = float(evento["lotacao_percentual"])
            lotacao_valor = lotacao_percent / 100
            cor = cor_lotacao(lotacao_percent)

            clima = clima_evento()

            app_view.controls.append(
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: pagina_home(),
                        ),

                        
                        ft.Container(
                            height=220,
                            margin=15,
                            border_radius=20,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=evento.get("imagem", ""),
                                fit="cover"
                            ),
                        ),

                        ft.Container(
                            padding=20,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    ft.Text(
                                        evento["nome"],
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color="white"
                                    ),

                                    ft.Text(
                                        f'{evento["data"]} • {evento["local"]}',
                                        color="white",
                                    ),

                                    ft.Text(
                                        f'R$ {evento["preco"]}',
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color="white"
                                    ),

                                    ft.Divider(color="white"),

                                    ft.Text("Clima previsto no dia:", weight=ft.FontWeight.BOLD, color="white"),
                                    ft.Text(clima, color="white"),

                                    ft.Divider(color="white"),

                                    ft.Text("Lotação em tempo real", weight=ft.FontWeight.BOLD, color="white"),

                                    ft.ProgressBar(value=lotacao_valor, color=cor),

                                    ft.Text(f"{evento['lotacao_percentual']}% ocupado", color="white"),
                                    
                                    ft.Container(height=10),

                                    ft.Button(
                                        "Adicionar ao carrinho",
                                        icon=ft.Icons.SHOPPING_CART,
                                        on_click=lambda e: adicionar_carrinho(evento)
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            )

            page.update()

    # CARD EVENTO
    def card_evento(evento, largura=250):
        
        img_url = evento.get("imagem") if evento.get("imagem") else "https://via.placeholder.com/150"

        return ft.Container(
            width=largura, 
            margin=ft.margin.only(left=15, right=15, top=10, bottom=10),
            padding=15,
            border_radius=20,
            bgcolor="white12", 
            blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
            
            content=ft.GestureDetector(
                on_tap=lambda e, ev=evento: pagina_evento(ev),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Container(
                            height=150, 
                            border_radius=15,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=img_url,
                                fit="cover",
                                
                                width=float("inf"), 
                                opacity=1.0, 
                            )
                        ),
                        
                        ft.Text(evento["nome"], weight=ft.FontWeight.BOLD, size=18, color="white"),
                        
                        ft.Text(
                            f'{evento["data"]} • {evento["local"]}',
                            size=12,
                            color="white70",
                        ),
                        
                        ft.Text(
                            f'R$ {evento["preco"]}',
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            color="white",
                        ),
                    ],
                ),
            ),
        )

    def card_evento(evento, largura=250):
        img_url = evento.get("imagem") or evento.get("Imagem") or "https://via.placeholder.com/150"

        return ft.Container(
            width=largura, 
           
            margin=ft.margin.only(left=15, right=15, top=10, bottom=10),
            padding=15,
            border_radius=20,
            bgcolor="white70", 
            blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
            content=ft.GestureDetector(
                on_tap=lambda e, ev=evento: pagina_evento(ev),
                content=ft.Column(
                    tight=True, 
                    spacing=8,
                    controls=[
                        ft.Container(
                            height=120, 
                            border_radius=15,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=img_url,
                                fit="cover",
                                width=float("inf"), 
                            )
                        ),
                        
                        ft.Text(
                            evento["nome"], 
                            weight="bold", 
                            size=16, 
                            color="black",
                            max_lines=1, 
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        
                        ft.Text(
                            f'{evento["data"]} • {evento["local"]}',
                            size=11,
                            color="#444444",
                        ),
                        
                        ft.Text(
                            f'R$ {evento["preco"]}',
                            weight="bold",
                            size=14,
                            color="black",
                        ),
                    ],
                ),
            ),
        )
    
    # CONFIGURAÇÕES
    def abrir_configuracoes(e, page): 
        def mudar_tema(e):
            page.theme_mode = (
                ft.ThemeMode.DARK 
                if page.theme_mode == ft.ThemeMode.LIGHT 
                else ft.ThemeMode.LIGHT
            )
            dialog.open = False
            page.update()

        def fechar_dialogo(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Configurações"),
            content=ft.Column(
                [
                    ft.Button(
                        "Alternar tema",
                        icon=ft.Icons.BRIGHTNESS_4,
                        on_click=mudar_tema
                    ),
                    ft.TextButton("Fechar", on_click=fechar_dialogo)
                ],
                tight=True,
            ),
        )
        page.overlay.append(dialog) 
        dialog.open = True
        page.update()

    # PERFIL
    def pagina_perfil():

        app_view.controls.clear()

        perfil_conteudo = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Container(
                    alignment=ft.Alignment(-1, 0),
                    padding=20,
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda e: pagina_home(),
                    ),
                ),

                ft.CircleAvatar(
                    radius=60,
                    bgcolor="white",
                    content=ft.Text(
                        usuario_logado["nome"][0].upper(),
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        color="#8ca6db"
                    ),
                ),

                ft.Container(height=10),

                ft.Text(
                    usuario_logado["nome"],
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),

                ft.Text(
                    usuario_logado["email"],
                    color="white70"
                ),

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
                                on_click=lambda e: pagina_meus_ingressos()
                            ),

                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.FAVORITE),
                                title=ft.Text("Eventos Favoritos"),
                            ),

                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.SETTINGS),
                                title=ft.Text("Configurações"),
                                on_click=lambda e: abrir_configuracoes(e, page) 
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

        bottom_bar = ft.Container(
            height=70,
            bgcolor="white",
            opacity=0.5,      
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[

                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        icon_size=28,
                        on_click=lambda e: pagina_home(),
                    ),

                    ft.IconButton(
                        icon=ft.Icons.CONFIRMATION_NUMBER,
                        icon_size=28,
                        on_click=lambda e: pagina_cupons(),
                    ),

                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_size=28,
                        on_click=lambda e: pagina_perfil(),
                    ),
                ],
            ),
        )

        app_view.controls.append(
            ft.Column(
                expand=True,
                controls=[
                    perfil_conteudo,
                    bottom_bar
                ]
            )
        )

    page.update()

     # CUPONS

    def nivel_usuario():
        total = obter_total_ingressos()

        if total < 3:
            return "Bronze", "🥉"
        elif total < 6:
            return "Prata", "🥈"
        elif total < 10:
            return "Ouro", "🥇"
        else:
            return "Diamond", "💎"

    def pagina_cupons():
        app_view.controls.clear()
        nivel, emoji = nivel_usuario()

        def abrir_confirmacao(nome_cupom):
            def fechar_dialog(e):
                confirmacao_dialog.open = False
                page.update()
            if nome_cupom not in cupons_resgatados:
                cupons_resgatados.append(nome_cupom)
    

            confirmacao_dialog = ft.AlertDialog(
                modal=True,
                content=ft.Container(
                    width=320,
                    height=400,
                    padding=20,
                    bgcolor="white",
                    border_radius=25,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Icon(ft.Icons.REDEEM, size=70, color="#FF9D00"),
                            ft.Text("Cupom Resgatado!", size=22, weight="bold"),
                            ft.Text("Use o código abaixo na compra:", color="black54", text_align="center"),
                            ft.Container(
                                bgcolor="#FFF5F0",
                                padding=15,
                                border_radius=10,
                                content=ft.Text(nome_cupom, size=28, weight="bold", color="#E64A19")
                            ),
                            ft.Button(
                                content=ft.Text("Fechar"), 
                                on_click=fechar_dialog,
                                width=200,
                                bgcolor="black",
                                color="white"
                            )
                        ]
                    )
                )
            )
            
            if confirmacao_dialog not in page.overlay:
                page.overlay.append(confirmacao_dialog)
            
            confirmacao_dialog.open = True
            page.update()

        proximo_nivel = {
            "Bronze": 3,
            "Prata": 6,
            "Ouro": 10,
            "Diamond": 10
        }

        meta = proximo_nivel[nivel]

        total = obter_total_ingressos()

        barra = ft.ProgressBar(
            width=300,
            value=min(total / meta, 1),
            color="white",
            bgcolor="white24"
        )

        cupons = [
            {"nome": "MAKO5", "desc": "R$5 de desconto", "nivel": "Bronze"},
            {"nome": "MAKO10", "desc": "10% OFF em eventos", "nivel": "Prata"},
            {"nome": "VIP20", "desc": "20% OFF eventos VIP", "nivel": "Ouro"},
            {"nome": "DIAMOND30", "desc": "30% OFF + acesso antecipado", "nivel": "Diamond"},
        ]

        def pode_usar(nivel_cupom):
            ordem = ["Bronze","Prata","Ouro","Diamond"]
            return ordem.index(nivel) >= ordem.index(nivel_cupom)

        cards = []

        for cupom in cupons:
            liberado = pode_usar(cupom["nivel"])
            card = ft.Container(
                padding=20,
                margin=15,
                width=320,
                border_radius=20,
                bgcolor="white",
                opacity=1 if liberado else 0.5,
                shadow=ft.BoxShadow(
                    blur_radius=12,
                    color="black12",
                    offset=ft.Offset(0,4)
                ),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    cupom["nome"],
                                    size=20,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Icon(
                                    ft.Icons.LOCAL_OFFER,
                                    color="#8ca6db"
                                )
                            ]
                        ),
                        ft.Text(
                            cupom["desc"],
                            size=15,
                            color="black87"
                        ),
                        ft.Text(
                            f"Nível necessário: {cupom['nivel']}",
                            size=13,
                            color="black54"
                        ),
                        ft.Container(height=5),
                        ft.Button(
                            content=ft.Text("Resgatar" if liberado else "Bloqueado 🔒"),
                            icon=ft.Icons.REDEEM,
                            disabled=not liberado,
                            on_click=lambda e, n=cupom["nome"]: abrir_confirmacao(n), 
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=15
                            )
                        )
                    ]
                )
            )
            cards.append(card)

        total = obter_total_ingressos()

        app_view.controls.append(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(top=20), 
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color="white",
                                    on_click=lambda e: pagina_home()
                                ),
                                ft.Text(
                                    "🎁 Programa de Fidelidade",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                    expand=True
                                ),
                            ]
                        )
                    ),
                    ft.Text(
                        f"Seu nível atual: {emoji} {nivel}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#FFD700" if nivel=="Ouro" else "#474a50" if nivel=="Prata" else "#CD7F32" if nivel=="Bronze" else "#00E5FF"
                    ),
                    ft.Text(
                        f"Ingressos comprados: {total}",
                        color="white"
                    ),
                    barra,
                    ft.Text(
                        f"{total}/{meta} para próximo nível",
                        color="white70",
                        size=12
                    ),
                    ft.Container(height=20),
                    *cards
                ]
            )
        )
        page.update()
        
        
    #CARRINHO
    def pagina_carrinho():

        app_view.controls.clear()

        subtotal = sum(float(ev["preco"]) for ev in carrinho)
        taxa_envio = 15.00
        desconto = 0

        texto_desconto = ft.Text("", color="green400", size=14)

        campo_cupom = ft.TextField(
            label="Código de cupom",
            width=220,
            bgcolor="white",
            border_radius=10,
            filled=True
        )

        texto_total = ft.Text(
            f"R$ {subtotal + taxa_envio:.2f}",
            size=22,
            weight="bold",
            color="orange400"
        )

        def aplicar_cupom(e):
            nonlocal desconto

            codigo = campo_cupom.value.upper()

            if codigo == "MAKO5":
                desconto = 5

            elif codigo == "MAKO10":
                desconto = subtotal * 0.10

            elif codigo == "VIP20":
                desconto = subtotal * 0.20

            elif codigo == "DIAMOND30":
                desconto = subtotal * 0.30

            else:
                desconto = 0
                texto_desconto.value = "❌ Cupom inválido"
                texto_desconto.color = "red400"
                page.update()
                return

            total = subtotal + taxa_envio - desconto

            texto_total.value = f"R$ {total:.2f}"
            texto_desconto.value = f"✅ - R$ {desconto:.2f} aplicado"
            texto_desconto.color = "green400"

            campo_cupom.value = ""

            page.update()

        itens = []

        for evento in carrinho:
            card = ft.Container(
                padding=15,
                margin=10,
                border_radius=20,
                bgcolor="white",
                shadow=ft.BoxShadow(
                    blur_radius=15,
                    color="black12",
                    offset=ft.Offset(0, 5)
                ),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(evento["nome"], weight="bold", size=16),
                                ft.Text(f'R$ {evento["preco"]}', color="grey700"),
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red400",
                            tooltip="Remover",
                            on_click=lambda e, ev=evento: remover_item(ev)
                        )
                    ]
                )
            )
            itens.append(card)

        resumo = ft.Container(
            padding=20,
            margin=15,
            border_radius=20,
            bgcolor="white",
            shadow=ft.BoxShadow(
                blur_radius=20,
                color="black12",
                offset=ft.Offset(0, 5)
            ),
            content=ft.Column(
                spacing=12,
                controls=[

                    ft.Text("Resumo do Pedido", size=20, weight="bold"),

                    ft.Row(
                        [
                            ft.Text("Subtotal"),
                            ft.Text(f"R$ {subtotal:.2f}")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Row(
                        [
                            ft.Text("Taxa de envio"),
                            ft.Text(f"R$ {taxa_envio:.2f}")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Row(
                        [
                            ft.Text("Desconto"),
                            texto_desconto
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Divider(),

                    ft.Row(
                        [
                            ft.Text("Total Geral", weight="bold"),
                            texto_total
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Divider(),

                    ft.Text("Cupom de desconto", weight="bold"),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            campo_cupom,
                            ft.ElevatedButton(
                                "Aplicar",
                                on_click=aplicar_cupom,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    bgcolor="blue400",
                                    color="white"
                                )
                            )
                        ]
                    ),

                    ft.Container(height=10),

                    ft.ElevatedButton(
                        "Finalizar Compra",
                        icon=ft.Icons.PAYMENT,
                        width=300,
                        height=50,
                        style=ft.ButtonStyle(
                            bgcolor="purple500",
                            color="white",
                            overlay_color="white24",
                            shape=ft.RoundedRectangleBorder(radius=15)
                        ),
                        on_click=lambda e: sua_funcao_de_pagamento(e, campo_cupom.value)
                    )
                ]
            )
        )

        app_view.controls.append(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="white",
                                on_click=lambda e: pagina_home()
                            ),

                            ft.Text(
                                "Seu Carrinho 🛒",
                                size=28,
                                weight="bold",
                                color="white"
                            ),
                        ]
                    ),

                    ft.Divider(color="white24"),

                    *itens,

                    resumo
                ]
            )
        )

        page.update()
        
    # MEUS INGRESSOS 

    def gerar_qr(texto):
        qr = qrcode.make(texto)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    def pagina_meus_ingressos():
        if usuario_logado is None:
            page.snack_bar = ft.SnackBar(ft.Text("Faça login primeiro"))
            page.snack_bar.open = True
            page.update()
            return

        app_view.controls.clear()

        try:
            response = requests.get(f"{API_MEUS_INGRESSOS}&usuario_id={usuario_logado['id']}")
            ingressos = response.json() if response.status_code == 200 else []
        except:
            ingressos = []

        lista_cards = []

        if not ingressos:
            lista_cards.append(
                ft.Container(
                    content=ft.Text("Você ainda não possui ingressos 🎟", size=18, color="white70"),
                    margin=ft.margin.only(top=50),
                    alignment=ft.Alignment(0, 0) 
                )
            )

        for ingresso in ingressos:
            qr = gerar_qr(f"ingresso-{ingresso['ingresso_id']}")

            
            card = ft.Container(
                margin=ft.margin.only(bottom=20, left=10, right=10),
                padding=0, 
                border_radius=25,
                bgcolor="white", 
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Row(
                    spacing=0,
                    controls=[
                        ft.Container(width=15, bgcolor="purple600"),
                        
                        ft.Container(
                            padding=20,
                            expand=True,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        ingresso["nome"].upper(),
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color="black",
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Divider(height=1, color="black12"),
                                    
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color="grey"),
                                            ft.Text(f"{ingresso['data']}", size=13, color="grey700"),
                                            ft.VerticalDivider(width=10),
                                            ft.Icon(ft.Icons.LOCATION_ON, size=16, color="grey"),
                                            ft.Text(f"{ingresso['local']}", size=13, color="grey700"),
                                        ]
                                    ),

                                   
                                    ft.Container(
                                        padding=10,
                                        border=ft.border.all(1, "black12"),
                                        border_radius=15,
                                        bgcolor="#f5f5f5",
                                        content=ft.Image(
                                            src=qr,
                                            width=180,
                                            height=180,
                                        )
                                    ),

                                    ft.Text(
                                        f"ID DO INGRESSO: #{ingresso['ingresso_id']}",
                                        size=10,
                                        color="grey",
                                        weight=ft.FontWeight.W_300
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
            lista_cards.append(card)

   
        app_view.controls.append(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                controls=[
              
                    ft.Container(
                        padding=ft.padding.only(top=10, left=10, right=10, bottom=20),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                    icon_color="white",
                                    on_click=lambda e: pagina_home()
                                ),
                                ft.Text(
                                    "Meus Ingressos",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color="white"
                                ),
                                ft.IconButton(icon=ft.Icons.MORE_VERT, icon_color="white"),
                            ]
                        )
                    ),
                    

                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=lista_cards
                    )
                ]
            )
        )

        page.update()
        
    def filtrar_eventos(texto, lista_vertical):
        texto = texto.lower()

        lista_vertical.controls.clear()

        for e in eventos:
                if texto in e["nome"].lower():
                    lista_vertical.controls.append(card_evento(e, largura=None))

        page.update()
            
        
    # HOME
    def pagina_home():

        app_view.controls.clear()
        app_view.scroll = ft.ScrollMode.AUTO
        app_view.expand = True

        lista_vertical = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[card_evento(e, largura=None) for e in eventos],
        )


        # CAMPO DE BUSCA
        campo_busca = ft.TextField(
            hint_text="Pesquisar eventos...",
            expand=True,
            border_radius=30,
            border_color="white",
            filled=True,
            bgcolor="white",
            on_change=lambda e: filtrar_eventos(e.control.value, lista_vertical)
        )

        search_bar = ft.Container(
            padding=15,
            content=ft.Row(
                spacing=10,
                controls=[
                    campo_busca,
                    ft.IconButton(
                        icon=ft.Icons.SHOPPING_CART,
                        icon_color="white",
                        on_click=lambda e: pagina_carrinho()
                    ),
                ],
            ),
        )

        # CARROSSEL
        carrossel = ft.Container(
            height=220,
            content=ft.Row(
                scroll=ft.ScrollMode.AUTO,
                controls=[card_evento(e) for e in eventos],
            ),
        )

        # LISTA QUE VAI SER FILTRADA
        lista_vertical = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[card_evento(e, largura=None) for e in eventos],
        )

        # BOTTOM BAR
        bottom_bar = ft.Container(
            height=70,
            bgcolor="white",
            opacity=0.5,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        icon_size=28,
                        on_click=lambda e: pagina_home(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CONFIRMATION_NUMBER,
                        icon_size=28,
                        on_click=lambda e: pagina_cupons(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_size=28,
                        on_click=lambda e: pagina_perfil(),
                    ),
                ],
            ),
        )

        # MONTAGEM DA TELA
        app_view.controls.append(search_bar)

        app_view.controls.append(
            ft.Container(
                padding=ft.padding.only(left=15, bottom=5),
                content=ft.Text("🔥 Em Alta", size=18, weight=ft.FontWeight.BOLD, color="white"),
            )
        )

        app_view.controls.append(carrossel)

        app_view.controls.append(
            ft.Container(
                padding=ft.padding.only(left=15, top=10, bottom=5),
                content=ft.Text("🎟 Outros Eventos", size=18, weight=ft.FontWeight.BOLD, color="white"),
            )
        )

        lista_vertical.expand = False
        app_view.controls.append(lista_vertical)
        app_view.controls.append(ft.Container(height=20))
        app_view.controls.append(bottom_bar)

        page.update()
        
        
    # FUNÇÃO DE PAGAMENTO
    def animacao_compra():

        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                width=320,
                height=320,
                padding=20,
                border_radius=25,
                bgcolor="white",
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[

                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE,
                            color="green",
                            size=90
                        ),

                        ft.Text(
                            "Compra realizada!",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Seu ingresso foi adicionado à carteira 🎟",
                            text_align="center",
                            color="grey"
                        ),

                        ft.Container(height=10),

                        ft.Button(
                            "Ver meus ingressos",
                            on_click=lambda e: (
                                fechar_animacao(dialog),
                                pagina_meus_ingressos()
                            )
                        )
                    ]
                )
            )
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    def fechar_animacao(dialog):

        dialog.open = False
        page.update()

    
    
    def sua_funcao_de_pagamento(e, cupom):
        
        desconto = 0
        texto_desconto = ft.Text("", color="green")

        total = sum(float(ev["preco"]) for ev in carrinho)

        if cupom.upper() in cupons_resgatados:

            if cupom == "MAKO5":
                desconto = 5

            elif cupom == "MAKO10":
                desconto = total * 0.10

            elif cupom == "VIP20":
                desconto = total * 0.20

            elif cupom == "DIAMOND30":
                desconto = total * 0.30

        total_final = total - desconto
        
        if not carrinho:
            page.snack_bar = ft.SnackBar(ft.Text("Carrinho vazio"))
            page.snack_bar.open = True
            page.update()
            return
        for evento in carrinho:
            dados = {
                "usuario_id": usuario_logado["id"],
                "evento_id": evento["id"]
            }
            print("debug1:",  usuario_logado["id"])
            print("debug2:",  evento["id"])
            response = requests.post(   
                "http://127.0.0.1/appstore_wallet/index.php?action=comprar",
                json={
                    "action": "comprar",
                    "usuario_id": usuario_logado["id"],
                    "evento_id": evento["id"]
                }
            )

            print(response.text)
            
            try:
                resultado = response.json()
                if resultado.get("status") != "sucesso":
                    print("Erro ao comprar:", resultado)
            except:
                print("Erro na resposta da API")
            

        carrinho.clear()
        animacao_compra()
        

    pagina_login()

ft.run(main)