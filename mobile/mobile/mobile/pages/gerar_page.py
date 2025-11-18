import flet as ft
from .codigo_page import codigo_page

def gerar_page(dados_usuario, page=None, mudar_pagina=None):
    def ir_codigo(e):
        # muda para a página de código
        if mudar_pagina:
            mudar_pagina("codigo") # isso vai chamar a função do main.py
    
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.SETTINGS, size=60, color=ft.Colors.BLUE),
                ft.Text("Configurações ⚙️", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=30),
                ft.ElevatedButton(
                    text="Gerar código para visitante",
                    icon=ft.Icons.QR_CODE,
                    on_click=ir_codigo
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=40,
        visible=False
    )
    return conteudo
