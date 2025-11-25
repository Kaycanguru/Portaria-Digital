import flet as ft
from .codigo_page import codigo_page

def gerar_page(page=None, mudar_pagina=None):

    # ---- Barra Roxa ----
    barra_gerar = ft.Container(
        content=ft.Text(
            "Gerar código",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="#000000",  # roxo escuro
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor="#E4D8FF",      # mesmo lilás da barra de navegação
        padding=ft.padding.symmetric(vertical=12),
        width=page.width,
        expand=True
    )

    def ir_codigo(e):
        # muda para a página de código
        if mudar_pagina:
            mudar_pagina("codigo") # isso vai chamar a função do main.py
    
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.QR_CODE_2, size=200, color="#28044C"),
                barra_gerar,
                ft.Container(height=5),
                ft.ElevatedButton(
                    text="Gerar código para visitante",
                    icon=ft.Icons.QR_CODE_2,
                    on_click=ir_codigo
                ),

                # ---- Card lilás de instrução ----
                ft.Container(
                    content=ft.Container(
                        content=ft.Text(
                            "Agora você pode gerar um código temporário para permitir a entrada de seus visitantes no condomínio. "
                            "Basta acessar a opção “Gerar código para visitante” no aplicativo, criar um novo código e compartilhá-lo "
                            "com a pessoa que vai entrar.",
                            size=14,
                            color="#000000",
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=15,
                        bgcolor="#E4D8FF",
                        border_radius=10,
                    ),
                    padding=ft.padding.only(top=10)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=40,
        visible=False
    )
    return conteudo
