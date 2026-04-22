"""
Módulo do Chatbot de Inteligência Artificial para suporte ao usuário.
Gerencia a UI do chat flutuante, histórico de conversas e integração com o modelo generativo Gemini.
"""
import flet as ft

def update_chat_visibility(page):
    usuario_logado = getattr(page, 'usuario_logado', None)
    chat_aberto = getattr(page, 'chat_aberto', None)
    botao_chat = getattr(page, 'botao_chat', None)
    chat_box = getattr(page, 'chat_box', None)
    
    if not botao_chat or not chat_box:
        return

    if usuario_logado:
        botao_chat.visible = True
        chat_box.visible = chat_aberto
    else:
        botao_chat.visible = False
        chat_box.visible = False

    page.update()

def setup_chat(page, app_view, route):
    setattr(page, 'chat_aberto', False)
    
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
                    content=ft.Text("Olá, como posso ajudar com o seu ingresso hoje?", color="black", no_wrap=False)
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

    def responder_chat(msg):
        msg = msg.lower()
        if "evento" in msg:
            resposta = "Temos vários eventos em destaque. Acesse a tela inicial para conferir."
        elif "ola" in msg or "olá" in msg:
            resposta = "Olá! Acesse a aba de eventos para encontrar a sua próxima experiência."   
        elif "oi" in msg:
            resposta = "Olá, seja bem-vindo."     
        elif "ingresso" in msg:
            resposta = "Você pode gerenciar seus ingressos diretamente na aba Perfil."
        elif "carrinho" in msg:
            route(page, app_view, "carrinho")
            resposta = "Abrindo seu carrinho de compras."
        elif "cupom" in msg:
            resposta = "Cupons ativos: MAKO10, VIP20, DIAMOND30."
        elif "valores" in msg:
            resposta = "Os valores podem ser consultados na página dedicada de cada evento."
        else:
            resposta = "Por favor, entre em contato com nosso Suporte para mais detalhes."

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
        responder_chat(texto)
        campo_msg.value = ""
        page.update()

    def toggle_chat(e):
        if getattr(page, 'usuario_logado', None) is None:
            return
        chat_aberto = not getattr(page, 'chat_aberto', False)
        setattr(page, 'chat_aberto', chat_aberto)
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
                    gradient=ft.LinearGradient(colors=["#93c5fd", "#818cf8"]),
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SUPPORT_AGENT, color="white", size=24),
                            ft.Container(width=10),
                            ft.Text("Atendimento ao Cliente", color="white", weight=ft.FontWeight.BOLD)
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
                                bgcolor="#818cf8",
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
                    gradient=ft.LinearGradient(colors=["#93c5fd", "#818cf8"]),
                    shadow=ft.BoxShadow(blur_radius=15, color="purple200"),
                    content=ft.FloatingActionButton(
                        icon=ft.Icons.SUPPORT_AGENT,
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
    
    setattr(page, 'botao_chat', botao_chat)
    setattr(page, 'chat_box', chat_box)
    
    update_chat_visibility(page)
