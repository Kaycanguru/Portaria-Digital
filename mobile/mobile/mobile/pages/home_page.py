import flet as ft

def home_page(dados_usuario, page, mudar_pagina):
    texto_pontos = ft.Text(f"Pontos: {dados_usuario['pontos']} ⭐", size=16)

    # ---- Função para ganhar pontos ----
    def adicionar_pontos(e):
        dados_usuario["pontos"] += 10
        texto_pontos.value = f"Pontos: {dados_usuario['pontos']} ⭐"
        page.update()

    # ---- Função do botão Sair ----
    def sair(e):
        mudar_pagina("login")   # volta para a tela de login

    # ---- Botão Sair estilizado ----
    botao_sair = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.LOGOUT, size=20),
                ft.Text("Sair", size=16),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        ),
        width=140,
        height=45,
        bgcolor="#FF4E4E",
        color=ft.Colors.WHITE,
        on_click=sair
    )

    # ---- Layout completo da página home ----
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.BLUE,
                    radius=60
                ),
                ft.Text(dados_usuario["nome"], size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Nível: {dados_usuario['nivel']}", size=16, color=ft.Colors.BLUE_600),
                texto_pontos,

                ft.Container(height=20),

                ft.ElevatedButton(
                    "Ganhar Pontos! ",
                    on_click=adicionar_pontos,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE
                ),

                ft.Container(height=20),

                # --- Aqui entra o botão de sair ---
                botao_sair
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=False
    )

    return conteudo, texto_pontos
