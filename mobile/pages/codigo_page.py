import flet as ft
import random
import string
import requests  # para enviar ao Flask

# -----------------------------------------------------------------------------------
# FUNÇÃO PRINCIPAL DA PÁGINA DE GERAR CÓDIGOS
# -----------------------------------------------------------------------------------
def codigo_page(page: ft.Page, mudar_pagina, get_morador_logado):
    codigo_gerado = ft.Text("", size=20, weight=ft.FontWeight, color="#28044C") # mostra o código depois de gerar

    # -----------------------------------------------------------------------------------
    # DROPDOWN PARA SELECIONAR A VALIDADE DO CÓDIGO
    # -----------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------
    # FUNÇÃO: GERAR CÓDIGO DE 6 CARACTERES (LETRAS + NÚMEROS)
    # -----------------------------------------------------------------------------------
    def gerar_codigo(e):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) # gera um código de 6 caracteres
        validade_texto = validade_dropdown.value or "2 horas"
        validade_horas = int(validade_texto.split()[0])

         # Exibe o código na tela
        codigo_gerado.value = f"Código: {codigo}\nValidade: {validade_horas} horas"
        codigo_gerado.color = "#28044C"
        codigo_gerado.size = 16
        page.update()

        morador_id_logado = get_morador_logado()

        # -----------------------------------------------------------------------------------
        # ENVIA O CÓDIGO PARA O BACKEND FLASK SALVAR NO BANCO
        # -----------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------
    # FUNÇÃO PARA VOLTAR À TELA ANTERIOR
    # -----------------------------------------------------------------------------------
    def sair(e):
        mudar_pagina("gerar")

    # -----------------------------------------------------------------------------------
    # BOTÕES: GERAR CÓDIGO + VOLTAR
    # -----------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------
    # LAYOUT PRINCIPAL DA PÁGINA
    # -----------------------------------------------------------------------------------
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.QR_CODE_2, size=100, color="#28044C"),
                ft.Text("Gerar Código de Visita", size=24, weight=ft.FontWeight.BOLD, color="#28044C"),
                ft.Container(height=20),

                # Área com dropdown + botões
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
