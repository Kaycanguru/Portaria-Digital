import flet as ft
import random
import string
import requests  # para enviar ao Flask

def codigo_page(page: ft.Page, mudar_pagina):
    codigo_gerado = ft.Text("", size=20, weight=ft.FontWeight, color="#28044C")

    # ----- DROPDOWN: validade -----
    validade_dropdown = ft.Dropdown(
        label="Validade do código",
        width=250,
        border_color="#28044C",
        border_radius=15,
        options=[
            ft.dropdown.Option("2 horas"),
            ft.dropdown.Option("6 horas"),
            ft.dropdown.Option("12 horas"),
            ft.dropdown.Option("24 horas"),
        ]
    )

    # Função para gerar código
    def gerar_codigo(e):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        validade_texto = validade_dropdown.value or "2 horas"
        validade_horas = int(validade_texto.split()[0])

        codigo_gerado.value = f"Código: {codigo}\nValidade: {validade_horas} horas"
        codigo_gerado.color = "#28044C"
        codigo_gerado.size = 16
        page.update()

        # pega o morador logado da sessão
        morador_id_logado = page.session.get("morador_id_logado")

        # envia para backend Flask
        try:
            res = requests.post(
                "http://127.0.0.1:5000/codigos/criar",
                json={
                    "codigo": codigo,
                    "morador_id": morador_id_logado,
                    "validade_horas": validade_horas
                }
            )
            print(res.json())
        except Exception as err:
            print("Erro ao salvar código:", err)

    # Função para voltar
    def sair(e):
        mudar_pagina("gerar")

    # ----- BOTÕES (GERAR + VOLTAR) -----
    botoes_coluna = ft.Column(
        controls=[
            ft.ElevatedButton(
                "Gerar Código",
                on_click=gerar_codigo,
                color=ft.Colors.WHITE,
                bgcolor="#28044C",
                width=250,
                height=30
            ),
            ft.ElevatedButton(
                "Voltar",
                on_click=sair,
                color="#28044C",
                bgcolor=ft.Colors.WHITE,
                width=250,
                height=30,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, "#28044C"),  # Borda roxa
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12
    )

    # ----- LAYOUT -----
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.QR_CODE, size=100, color="#28044C"),
                ft.Text("Gerar Código de Visita", size=24, weight=ft.FontWeight.BOLD, color="#28044C"),
                ft.Container(height=20),

                ft.Column(
                    controls=[
                        validade_dropdown,
                        botoes_coluna
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),

                ft.Container(height=20),
                codigo_gerado
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=False
    )

    return conteudo
