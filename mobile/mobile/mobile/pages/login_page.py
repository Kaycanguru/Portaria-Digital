import flet as ft
import mysql.connector # Foi instalado

# Função para conectar ao banco
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Senai@118",
        database="portaria"
    )

def login_page(page, mudar_pagina):
    email_input = ft.TextField(label="E-mail", width=300, border_color="#28044C", border_radius=15)
    senha_input = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True, border_color="#28044C", border_radius=15)
    mensagem = ft.Text("", color="red", size=14)

    # Função do botão de login
    def entrar(e):
        email = email_input.value.strip()
        senha = senha_input.value.strip()

        if not email or not senha:
            mensagem.value = "Preencha todos os campos!"
            page.update()
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, morador_id FROM usuarios_mobile WHERE email_usuario=%s AND senha_usuario=%s", (email, senha))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                mensagem.value = ""

                # salvar o morador logado
                page.session.set("morador_id_logado", usuario[1])

                # ir para home
                mudar_pagina("home")

            else:
                mensagem.value = "Usuário ou senha incorretos!"

        except Exception as ex:
            mensagem.value = f"Erro de conexão: {ex}"

        page.update()

    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(src="images/logo.png", width=200, height=200, fit=ft.ImageFit.CONTAIN),
                ft.Text("Bem-vindo!", size=28, weight=ft.FontWeight.BOLD, color="#28044C"),
                ft.Text("Controle de entrada com praticidade e segurança!",
                        size=22, text_align=ft.TextAlign.CENTER, color="#28044C"),
                ft.Text("Login", size=26, text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_600, color="#28044C"),
                ft.Container(height=10),
                email_input,
                senha_input,
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
