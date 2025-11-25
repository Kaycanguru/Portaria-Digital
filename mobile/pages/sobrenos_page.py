import flet as ft

def sobrenos_page(page, mudar_pagina):
    
    def voltar(e):
        mudar_pagina("config")   # VOLTA para a página config

    # ----- Cabeçalho -----
    titulo = ft.Text(
        "Sobre nós",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#28044C"
    )

    cabecalho = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_size=26,
                    icon_color="#28044C",
                    on_click=voltar
                ),
                titulo
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#E4D8FF",
        padding=20,
        alignment=ft.alignment.center_left,
        visible=False
    )

    # ----- Estilos de texto -----
    def titulo_card(texto):
        return ft.Text(
            texto,
            size=18,
            weight=ft.FontWeight.W_600,
            color="black"
        )

    def texto_card(texto):
        return ft.Text(
            texto,
            size=16,
            color="black"
        )

    # ----- Card estilizado -----
    def card_estilizado(conteudo):
        return ft.Container(
            content=conteudo,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 3),
            ),
            width=page.width
        )

    # ----- Conteúdo do card -----
    card_sobre = card_estilizado(
        ft.Column(
            controls=[
                titulo_card("Sobre o condomínio Atrivium Residencial"),

                texto_card(
                    "O aplicativo foi criado para facilitar o dia a dia dos moradores, "
                    "trazendo praticidade e segurança para o controle de acesso "
                    "e comunicação interna."
                ),

                titulo_card("O que você encontra no app:"),
                texto_card("• Códigos temporários para visitantes"),
                texto_card("• Contatos e informações úteis da administração"),
                texto_card("• Avisos e atualizações importantes do condomínio"),

                titulo_card("Objetivo"),
                texto_card(
                    "Nosso objetivo é tornar a rotina mais simples e moderna"
                    "para todos os moradores, oferecendo um sistema intuitivo e fácil de usar."
                ),
            ],
            spacing=10
        )
    )

    # ----- Conteúdo final da página -----
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                card_sobre
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=20,
        visible=False
    )

    return conteudo, cabecalho
