import flet as ft
import mysql.connector

# ---------------------------------------------
# FUNÇÃO DE CONEXÃO COM O MYSQL
# ---------------------------------------------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Senai@118",
        database="portaria"
    )

# ---------------------------------------------
# PÁGINA DE CONFIGURAÇÃO
# ---------------------------------------------
def config_page(page, mudar_pagina, get_morador_logado):
    # Coluna que exibirá os dados do morador — começa com "Carregando..."
    texto_card = ft.Column(controls=[ft.Text("Carregando...", size=16, color=ft.Colors.BLACK)])

    # Card que mostrará informações do morador
    card_morador = ft.Container(
        content=ft.Column(
            controls=[texto_card],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        ),
        width=page.width,
        alignment=ft.alignment.center
    )

    # Conteúdo principal da página
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                
                # --- TÍTULO CONTA ---
                ft.Container(
                        content=ft.Text("Conta", size=20, weight=ft.FontWeight.W_600, color="#28044C"),
                        alignment=ft.alignment.center_left
                    ),
                
                ft.Container(height=20),

                # --- CARD MORADOR ---
                card_morador,

                ft.Container(height=30),

                # --- TÍTULO NOTIFICAÇÕES ---
                ft.Container(
                    content=ft.Text("Notificações", size=20, weight=ft.FontWeight.W_600, color="#28044C"),
                    alignment=ft.alignment.center_left
                ),

                ft.Container(height=10),

                # --- CARD NOTIFICAÇÕES ---
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Receber notificações", size=18, color="#28044C"),
                            ft.Switch(value=True)  # switch ligado por padrão
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    width=page.width,
                    alignment=ft.alignment.center
                ),

                ft.Container(height=30),

                # --- TÍTULO RESIDÊNCIA ---
                ft.Container(
                    content=ft.Text("Residência", size=20, weight=ft.FontWeight.W_600, color="#28044C"),
                    alignment=ft.alignment.center_left
                ),

                ft.Container(height=10),

                # --- CARD RESIDÊNCIA - Informações ---
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Informações do condomínio", size=18, color="#28044C"),
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, color="#28044C")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    width=page.width,
                    alignment=ft.alignment.center,
                    on_click=lambda e: mudar_pagina("info_condominio")
                ),

                ft.Container(height=10),

                # --- CARD RESIDÊNCIA - Contatos ---
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Contatos da portaria", size=18, color="#28044C"),
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, color="#28044C")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    width=page.width,
                    alignment=ft.alignment.center,
                    on_click=lambda e: mudar_pagina("contatos")
                ),

                ft.Container(height=30),

                # --- TÍTULO PRIVACIDADE E SEGURANÇA ---
                ft.Container(
                    content=ft.Text("Privacidade e segurança", size=20, weight=ft.FontWeight.W_600, color="#28044C"),
                    alignment=ft.alignment.center_left
                ),

                ft.Container(height=10),

                # --- CARD PRIVACIDADE E SEGURANÇA ---
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Reconhecimento Facial", size=18, color="#28044C"),
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, color="#28044C")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    width=page.width,
                    alignment=ft.alignment.center,
                    on_click=lambda e: mudar_pagina("rec_facial")
                ),

                ft.Container(height=30),

                # --- TÍTULO OUTROS ---
                ft.Container(
                    content=ft.Text("Outros", size=20, weight=ft.FontWeight.W_600, color="#28044C"),
                    alignment=ft.alignment.center_left
                ),

                ft.Container(height=10),

                # --- CARD OUTROS ---
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Sobre nós", size=18, color="#28044C"),
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, color="#28044C")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    width=page.width,
                    alignment=ft.alignment.center,
                    on_click=lambda e: mudar_pagina("sobrenos")
                ),

                ft.Container(height=30),

                # ========== BOTÃO SAIR ==========
                ft.ElevatedButton(
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
                    bgcolor="#CA1F1F",
                    color=ft.Colors.WHITE,
                    on_click=lambda e: mudar_pagina("login")
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1
        ),
        padding=40,
        visible=False
    )

    # ---------------------------------------------
    # FUNÇÃO PARA CARREGAR DADOS DO MORADOR
    # ---------------------------------------------
    def carregar_dados_morador():
        morador_id = get_morador_logado() # Recupera o morador logado
        if not morador_id:
            texto_card.controls = [ft.Text("Morador não logado", size=16, color=ft.Colors.RED)]
            page.update()
            return

        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.nome_morador, m.bloco_morador, m.apartamento_morador
                FROM moradores m
                WHERE m.id = %s
            """, (morador_id,))
            morador = cursor.fetchone()

            cursor.close()
            conn.close()

            if morador:
                # substitui o conteúdo do texto_card por um Row com ícone + coluna de textos
                texto_card.controls = [
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=70, color="#28044C"),
                            ft.Column(
                                controls=[
                                    ft.Text(f"Nome: {morador['nome_morador']}", size=18, color="#28044C"),
                                    ft.Text(f"Bloco: {morador['bloco_morador']}", size=18, color="#28044C"),
                                    ft.Text(f"Apartamento: {morador['apartamento_morador']}", size=18, color="#28044C"),
                                ],
                                spacing=4,
                                alignment=ft.MainAxisAlignment.START
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=12
                    )
                ]
            else:
                texto_card.controls = [ft.Text("Dados do morador não encontrados", size=16, color=ft.Colors.RED)]

        except Exception as e:
            texto_card.controls = [ft.Text(f"Erro ao carregar dados: {e}", size=14, color=ft.Colors.RED)]

        page.update()

    # Retorna a página e a função de atualização
    return conteudo, carregar_dados_morador
