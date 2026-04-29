"""
Tela de Detalhes do Evento.
Exibe imagens heroicas, dados da festa, capacidade restante e botões para favoritar ou comprar.
"""
import flet as ft
from utils import cor_lotacao, clima_evento, show_msg, safe_storage_set

def render_evento(page, app_view, route, evento):
    if not evento:
        route(page, app_view, "home")
        return

    capacidade = evento.get("capacidade", 1)
    ingressos_vendidos = evento.get("ingressos_vendidos", 0)
    
    # Previne divisão por zero
    if capacidade <= 0:
        capacidade = 1
        
    lotacao_percent = (ingressos_vendidos / capacidade) * 100
    lotacao_valor = ingressos_vendidos / capacidade
    cor = cor_lotacao(lotacao_percent)
    clima = clima_evento()

    # Seletor de Quantidade
    txt_qtd = ft.Text("1", size=18, weight="bold", width=30, text_align="center")
    txt_preco_total = ft.Text(f"R$ {evento['preco']}", size=22, weight="bold", color="on_surface")
    
    def alterar_qtd(delta):
        nova_qtd = int(txt_qtd.value) + delta
        if nova_qtd >= 1:
            txt_qtd.value = str(nova_qtd)
            # Atualiza o preço total exibido
            preco_unitario = float(str(evento['preco']).replace(',', '.'))
            txt_preco_total.value = f"R$ {preco_unitario * nova_qtd:.2f}".replace('.', ',')
            page.update()

    def adicionar_carrinho(e):
        qtd = int(txt_qtd.value)
        carrinho = getattr(page, 'carrinho', None) or []
        
        for _ in range(qtd):
            carrinho.append(evento)
            
        setattr(page, 'carrinho', carrinho)
        # Persistência
        safe_storage_set(page, "carrinho_data", carrinho)
        
        msg = f"{qtd} ingressos para {evento['nome']} adicionados! 🚀" if qtd > 1 else f"Festa garantida! {evento['nome']} adicionado ao carrinho 🚀"
        show_msg(page, msg, bgcolor="#818cf8")
        
        # Pequeno delay para o feedback visual antes de mudar de tela
        import time
        # page.update() # Opcional se show_msg já faz
        route(page, app_view, "carrinho")

    # Header Hero com Stack
    hero_section = ft.Stack(
        controls=[
            ft.Container(
                height=260,
                content=ft.Image(
                    src=evento.get("imagem", ""),
                    fit="cover",
                    width=float("inf"),
                ),
            ),
            # Gradiente de sobreposição para leitura
            ft.Container(
                height=260,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, 0.5),
                    end=ft.Alignment(0, 1),
                    colors=["transparent", "#cc000000"],
                ),
            ),
            # Botão de Voltar Flutuante
            ft.Container(
                top=30,
                left=20,
                content=ft.Container(
                    bgcolor="#33ffffff",
                    blur=ft.Blur(10, 10),
                    border_radius=15,
                    padding=5,
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                        icon_color="white",
                        icon_size=20,
                        on_click=lambda e: route(page, app_view, "home")
                    ),
                ),
            ),
        ]
    )

    # Conteúdo Detalhado
    content_section = ft.Container(
        padding=ft.padding.only(left=25, right=25, top=20, bottom=180),
        content=ft.Column(
            spacing=25,
            controls=[
                # Título e Preço
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(evento["nome"], size=30, weight=ft.FontWeight.BOLD, color="on_surface"),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, size=16, color="#818cf8"),
                            ft.Text(evento["local"], size=14, color="on_surface_variant"),
                        ]),
                    ]
                ),
                
                # Cards de Info Rápida
                ft.Row(
                    spacing=15,
                    controls=[
                        ft.Container(
                            expand=1,
                            padding=15,
                            bgcolor="surface_variant",
                            border_radius=15,
                            content=ft.Column([
                                ft.Icon(ft.Icons.CALENDAR_MONTH, color="#818cf8"),
                                ft.Text("Data", size=12, color="on_surface_variant"),
                                ft.Text(evento["data"], size=14, weight="bold"),
                            ], spacing=5)
                        ),
                        ft.Container(
                            expand=1,
                            padding=15,
                            bgcolor="surface_variant",
                            border_radius=15,
                            content=ft.Column([
                                ft.Icon(ft.Icons.THERMOSTAT, color="#f87171"),
                                ft.Text("Clima", size=12, color="on_surface_variant"),
                                ft.Text(clima, size=14, weight="bold"),
                            ], spacing=5)
                        ),
                    ]
                ),

                # Lotação
                ft.Container(
                    padding=20,
                    bgcolor="surface",
                    border=ft.border.all(1, "outline_variant"),
                    border_radius=20,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Disponibilidade", weight="bold"),
                            ft.Text(f"{lotacao_percent:.0f}%", color=cor, weight="bold"),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=lotacao_valor, color=cor, bgcolor="outline_variant", height=8),
                        ft.Text("Garanta o seu antes que esgote!", size=12, color="on_surface_variant"),
                    ], spacing=10)
                ),

                # Seção de Descrição Refatorada e Enriquecida
                ft.Column([
                    ft.Row([
                        ft.Text("Sobre a Experiência", size=20, weight="bold"),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            bgcolor="#818cf822",
                            border_radius=8,
                            content=ft.Row([
                                ft.Icon(ft.Icons.AUTO_AWESOME, size=14, color="#818cf8"),
                                ft.Text("Hype Alta", size=10, weight="bold", color="#818cf8")
                            ], spacing=4)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.Text(
                        evento.get("descricao") or (
                            f"Aproveite o melhor de {evento['nome']} em {evento['local']}. "
                            "Um evento cuidadosamente planejado para oferecer uma experiência imersiva, "
                            "com infraestrutura de ponta e os melhores profissionais do setor. "
                            "Garanta seu lugar e faça parte de algo extraordinário."
                        ),
                        color="on_surface_variant"
                    ),
                    
                    # Badges de Destaque
                    ft.Container(height=10),
                    ft.Row([
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            bgcolor="#f8fafc",
                            border_radius=12,
                            border=ft.border.all(1, "#e2e8f0"),
                            content=ft.Row([
                                ft.Icon(ft.Icons.VERIFIED_USER_OUTLINED, size=16, color="#0f172a"),
                                ft.Text("Segurança VIP", size=12, weight="w500", color="#0f172a")
                            ], spacing=6)
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            bgcolor="#f8fafc",
                            border_radius=12,
                            border=ft.border.all(1, "#e2e8f0"),
                            content=ft.Row([
                                ft.Icon(ft.Icons.QR_CODE_2_ROUNDED, size=16, color="#0f172a"),
                                ft.Text("Entrada Digital", size=12, weight="w500", color="#0f172a")
                            ], spacing=6)
                        ),
                    ], spacing=10),
                    
                    # Info Úteis
                    ft.Container(height=15),
                    ft.Text("Informações Importantes", size=18, weight="bold"),
                    ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color="#64748b", size=20),
                            title=ft.Text("Formas de Pagamento", size=14, weight="bold"),
                            subtitle=ft.Text("PIX com 5% OFF ou cartão em até 12x.", size=12),
                            dense=True,
                            visual_density=ft.VisualDensity.COMPACT,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.MONETIZATION_ON_OUTLINED, color="#64748b", size=20),
                            title=ft.Text("Políticas de Reembolso", size=14, weight="bold"),
                            subtitle=ft.Text("Cancelamento grátis em até 7 dias após a compra.", size=12),
                            dense=True,
                            visual_density=ft.VisualDensity.COMPACT,
                        ),
                    ], spacing=0)
                ], spacing=12),
            ]
        )
    )

    # Barra de Compra Fixa (Botão Stick no Rodapé)
    action_bar = ft.Container(
        bottom=0,
        left=0,
        right=0,
        padding=ft.padding.only(left=25, right=25, top=15, bottom=25),
        bgcolor=ft.Colors.with_opacity(0.9, "surface"),
        blur=ft.Blur(10, 10),
        border=ft.border.only(top=ft.border.BorderSide(1, "outline_variant")),
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Total da seleção", size=12, color="on_surface_variant"),
                    txt_preco_total,
                ], spacing=2, expand=True),
                # Seletor de Quantidade
                ft.Container(
                    bgcolor="surface_variant",
                    border_radius=15,
                    padding=ft.padding.symmetric(horizontal=5, vertical=2),
                    content=ft.Row([
                        ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_size=24, icon_color="#818cf8", on_click=lambda _: alterar_qtd(-1)),
                        txt_qtd,
                        ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_size=24, icon_color="#818cf8", on_click=lambda _: alterar_qtd(1)),
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER)
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                gradient=ft.LinearGradient(colors=["#93c5fd", "#818cf8"]),
                border_radius=15,
                width=float("inf"),
                content=ft.ElevatedButton(
                    "Adicionar ao Carrinho",
                    color="white",
                    bgcolor="transparent",
                    elevation=0,
                    height=50,
                    on_click=adicionar_carrinho,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                    )
                ),
            )
        ], tight=True, spacing=15)
    )

    # Montando a View
    app_view.controls.append(
        ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=0,
                    controls=[
                        hero_section,
                        content_section
                    ]
                ),
                action_bar
            ]
        )
    )
