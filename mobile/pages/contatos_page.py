import flet as ft

def contatos_page(page, mudar_pagina):
    
    def voltar(e):
        mudar_pagina("config")

    # Cabeçalho
    titulo = ft.Text(
        "Contatos da portaria",
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

    # ----- FUNÇÕES DE ESTILO -----
    def card_titulo(texto):
        return ft.Text(
            texto,
            size=18,
            weight=ft.FontWeight.W_600,
            color="black"     # cor preta
        )

    def card_conteudo(texto):
        return ft.Text(
            texto,
            size=16,
            color="black"     # cor preta
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
            width=page.width   
        )

    # ---- Portaria principal ----
    portaria = card_estilizado(
        ft.Column([
            card_titulo("Portaria principal"),
            card_conteudo("Portaria 24h: (11) 98455-1234"),
            card_conteudo("WhatsApp da Portaria: (11) 94000-7788"),
            card_conteudo("Administração: adm.condominio@gmail.com"),
            card_conteudo("Ramal do porteiro: 101"),
        ], spacing=8)
    )

    # ---- Síndico e subsíndico ----
    sindicos = card_estilizado(
        ft.Column([
            card_titulo("Síndico e subsíndico"),
            card_conteudo("Síndico: Carlos Silva – (11) 97711-0099"),
            card_conteudo("Subsíndica: Carla Santos – (11) 99322-5500"),
        ], spacing=8)
    )

    # ---- Manutenção / Emergência ----
    manutencao = card_estilizado(
        ft.Column([
            card_titulo("Manutenção e emergência"),
            card_conteudo("Zelador: João Lima – (11) 98333-7733"),
            card_conteudo("Manutenção do elevador: manutencao@condominio.com"),
            card_conteudo("Vigilância interna: (11) 98888-2211"),
        ], spacing=8)
    )

    # Conteúdo final
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                portaria,
                ft.Container(height=5),
                sindicos,
                ft.Container(height=5),
                manutencao,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=20,
        visible=False
    )

    return conteudo, cabecalho
