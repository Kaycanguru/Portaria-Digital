import flet as ft
import mysql.connector

# -------------------------------
# FUNÇÃO DE CONEXÃO COM O BANCO
# -------------------------------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Senai@118",
        database="portaria"
    )

# ---------------------------------------------
# FUNÇÃO QUE MONTA A TELA DE LOGIN DO APLICATIVO
# ---------------------------------------------
def login_page(page, mudar_pagina, set_morador_func):  # recebe função setter
    email_input = ft.TextField(label="E-mail", width=300, border_color="#28044C", border_radius=15)
    senha_input = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True, border_color="#28044C", border_radius=15)
    mensagem = ft.Text("", color="red", size=14)

    # -----------------------------
    # FUNÇÃO QUE FECHA O CARD "ESQUECI A SENHA"
    # -----------------------------
    def fechar_card(e):
        card_esqueci.visible = False
        page.update()

    # Card exibido quando o usuário clica em "Esqueceu a senha?"
    card_esqueci = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Entre em contato com a sua organização para alterar a senha.",
                    size=14,
                    color="#000000",
                    expand=True,
                    text_align=ft.TextAlign.LEFT
                ),
                ft.GestureDetector(
                    on_tap=fechar_card,
                    content=ft.Text(
                        "✕",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#28044C"
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        bgcolor="#E4D8FF",
        padding=15,
        border_radius=10,
        visible=False
    )

    # -----------------------------
    # FUNÇÃO QUE ABRE O CARD DE "ESQUECI A SENHA"
    # -----------------------------
    def mostrar_card(e):
        card_esqueci.visible = True
        page.update()

    # -----------------------------
    # FUNÇÃO QUE VALIDA O LOGIN
    # -----------------------------
    def entrar(e):
        email = email_input.value.strip()
        senha = senha_input.value.strip()

        # Se algum campo estiver vazio
        if not email or not senha:
            mensagem.value = "Preencha todos os campos!"
            page.update()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Busca usuário no banco
            cursor.execute(
                "SELECT id, morador_id FROM usuarios_mobile WHERE email_usuario=%s AND senha_usuario=%s",
                (email, senha)
            )
            usuario = cursor.fetchone()
            conn.close()

            # Se encontrou usuário
            if usuario:
                mensagem.value = ""
                set_morador_func(usuario[1])  # atualiza morador logado
                mudar_pagina("home")
            # Senão, usuário inválido
            else:
                mensagem.value = "Usuário ou senha incorretos!"

        except Exception as ex:
            mensagem.value = f"Erro de conexão: {ex}"

        page.update()

    # ------------------------------------------------
    # ESTRUTURA VISUAL COMPLETA DA TELA DE LOGIN FLET
    # ------------------------------------------------
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(src="images/logo.png", width=200, height=200, fit=ft.ImageFit.CONTAIN),
                ft.Text("Bem-vindo!", size=28, weight=ft.FontWeight.BOLD, color="#28044C"),
                ft.Text("Controle de entrada com praticidade e segurança!", size=22, text_align=ft.TextAlign.CENTER, color="#28044C"),
                ft.Text("Login", size=26, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_600, color="#28044C"),
                ft.Container(height=10),
                email_input,
                senha_input,

                # Texto "Esqueceu a senha?"
                ft.GestureDetector(
                    on_tap=mostrar_card,
                    content=ft.Text(
                        "Esqueceu a senha?",
                        size=13,
                        color="#28044C",
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500,
                    )
                ),

                # Card exibido quando o usuário clica
                card_esqueci,

                ft.ElevatedButton("Entrar", on_click=entrar, color=ft.Colors.WHITE, bgcolor="#28044C", width=300),
                mensagem,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=True
    )

    return conteudo
