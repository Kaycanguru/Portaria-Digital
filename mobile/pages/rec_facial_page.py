import flet as ft

def rec_facial_page(page, mudar_pagina):
    
    def voltar(e):
        mudar_pagina("config")

    # ----- Cabeçalho -----
    titulo = ft.Text(
        "Reconhecimento Facial",
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
            alignment=ft.MainAxisAlignment.START
        ),
        bgcolor="#E4D8FF",
        padding=20,
        alignment=ft.alignment.center_left,
        visible=False
    )

    # ====== ESTILO DOS CARDS ======
    def card_titulo(texto):
        return ft.Text(
            texto,
            size=18,
            weight=ft.FontWeight.W_600,
            color="black"
        )

    def card_conteudo(texto):
        return ft.Text(
            texto,
            size=16,
            color="black"
        )

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
            width=page.width   # cards bem largos
        )

    # ====== CARDS DE INFORMAÇÃO ======

    # -- Introdução --
    intro = card_estilizado(
        ft.Column([
            card_titulo("Como funciona"),
            card_conteudo("O reconhecimento facial identifica os moradores automaticamente na entrada."),
            card_conteudo("Ele utiliza a câmera para analisar o rosto e comparar com o rosto já cadastrado."),
            card_conteudo("Se for reconhecido, o acesso é liberado imediatamente."),
        ], spacing=8)
    )

    # -- Funcionamento para o morador --
    como_funciona = card_estilizado(
        ft.Column([
            card_titulo("Para o morador"),
            card_conteudo("• Seu rosto precisa estar cadastrado pela administração."),
            card_conteudo("• Basta se aproximar da câmera para que o sistema faça a leitura."),
            card_conteudo("• Quando o rosto for reconhecido, a entrada será liberada."),
            card_conteudo("• Todas as entradas reconhecidas são registradas automaticamente."),
        ], spacing=8)
    )

    # -- Dicas --
    dicas = card_estilizado(
        ft.Column([
            card_titulo("Dicas para melhor reconhecimento"),
            card_conteudo("• Olhe para a câmera com o rosto visível."),
            card_conteudo("• Evite boné, capuz ou forte contra-luz."),
        ], spacing=8)
    )

    # -- Segurança --
    seguranca = card_estilizado(
        ft.Column([
            card_titulo("Segurança"),
            card_conteudo("• Somente rostos cadastrados podem entrar pelo reconhecimento facial."),
            card_conteudo("• Cada rosto tem uma “assinatura digital” única e segura."),
            card_conteudo("• Nenhuma imagem é enviada para fora do sistema."),
        ], spacing=8)
    )

    # -- Importante --
    importante = card_estilizado(
        ft.Column([
            card_titulo("Importante"),
            card_conteudo("Se o sistema não reconhecer você, procure a administração para atualizar o cadastro facial."),
        ], spacing=8)
    )

    # ====== CONTEÚDO FINAL ======
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                intro,
                ft.Container(height=5),
                como_funciona,
                ft.Container(height=5),
                dicas,
                ft.Container(height=5),
                seguranca,
                ft.Container(height=5),
                importante,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=20,
        visible=False
    )

    return conteudo, cabecalho
