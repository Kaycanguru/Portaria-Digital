import flet as ft
from pages.config_page import conectar
from datetime import datetime

# ---------------------------------------------------------
# PÁGINA PRINCIPAL "HOME" DO APLICATIVO
# ---------------------------------------------------------
def home_page(page, mudar_pagina):

    # -----------------------------------------
    # COLUNA INICIAL QUE MOSTRA O ÚLTIMO CÓDIGO
    # -----------------------------------------
    texto_card = ft.Column(
        controls=[ft.Text("Carregando código...", size=16, color="#333")],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    # -------------------------------------------------
    # CARD BRANCO QUE EXIBE O ÚLTIMO CÓDIGO GERADO
    # -------------------------------------------------
    card_codigo = ft.Container(
        content=texto_card,
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
        expand=True
    )

    # -----------------------------------------
    # LISTA ONDE OS ACESSOS SERÃO ADICIONADOS
    # -----------------------------------------
    lista_acessos = ft.Column(spacing=12)

    scroll_acessos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=lista_acessos,
                )
            ],
            # -----------------------------------------
            # SCROLL QUE ENVOLVE A LISTA DE ACESSOS
            # -----------------------------------------
            scroll=ft.ScrollMode.ALWAYS
        ),
        height=500,
        padding=5,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.20, ft.Colors.BLACK),
            offset=ft.Offset(0, 3)
        )
    )

    # ----------------------------
    # BARRA ROXA DO ÚLTIMO CÓDIGO
    # ----------------------------
    barra_ultimo_codigo = ft.Container(
        content=ft.Text("Último código gerado", size=18, weight=ft.FontWeight.BOLD, color="#000000", text_align=ft.TextAlign.CENTER),
        bgcolor="#E4D8FF",
        padding=ft.padding.symmetric(vertical=12),
        width=page.width
    )

    # ----------------------------
    # BARRA ROXA DOS ÚLTIMOS ACESSOS
    # ----------------------------
    barra_ultimos_acessos = ft.Container(
        content=ft.Text("Últimos acessos", size=18, weight=ft.FontWeight.BOLD, color="#28044C", text_align=ft.TextAlign.CENTER),
        bgcolor="#E4D8FF",
        padding=ft.padding.symmetric(vertical=12),
        width=page.width
    )

    # ---------------------------------------------
    # CONTEÚDO PRINCIPAL DO "HOME"
    # ---------------------------------------------
    conteudo = ft.Container(
        content=ft.Column(
            controls=[barra_ultimo_codigo, card_codigo, barra_ultimos_acessos, scroll_acessos],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=40,
        visible=False
    )

    # ---------------------------------------------
    # FUNÇÃO: CARREGAR ÚLTIMO CÓDIGO GERADO
    # ---------------------------------------------
    def carregar_ultimo_codigo(morador_id):
        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)

            # Pega o último código gerado pelo morador
            cursor.execute("""
                SELECT id, codigo, validade_horas, data_criacao
                FROM codigos
                WHERE morador_id = %s
                ORDER BY data_criacao DESC
                LIMIT 1
            """, (morador_id,))

            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            # Se encontrou um código
            if resultado:
                texto_card.controls = [
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.QR_CODE_2, size=50, color="#28044C"),
                            ft.Column(
                                controls=[
                                    ft.Text(f"Código: {resultado['codigo']}", size=18, color="#28044C"),
                                    ft.Text(f"Validade: {resultado['validade_horas']} horas", size=18, color="#28044C"),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ]

                # Carregar acessos também
                carregar_acessos_visitantes(morador_id)

            # Caso não exista código no banco
            else:
                texto_card.controls = [
                    ft.Text("Nenhum código encontrado", size=16, color="#333")
                ]

        except Exception as e:
            texto_card.controls = [
                ft.Text(f"Erro ao carregar: {e}", size=14, color="red")
            ]

        page.update()

    # ---------------------------------------------
    # FUNÇÃO: CARREGAR ACESSOS DO VISITANTE
    # ---------------------------------------------
    def carregar_acessos_visitantes(morador_id):
        lista_acessos.controls = []

        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)

            # Busca acessos recentes (últimos 20)
            cursor.execute("""
                SELECT av.data_hora, c.codigo
                FROM acessos_visitantes av
                JOIN codigos c ON av.codigo_id = c.id
                WHERE av.morador_id = %s
                ORDER BY av.data_hora DESC
                LIMIT 20
            """, (morador_id,))

            resultados = cursor.fetchall()

            cursor.close()
            conn.close()

            # Se não houve acessos
            if not resultados:
                lista_acessos.controls.append(
                    ft.Text("Nenhum acesso encontrado", size=14, color="#444")
                )

            # Caso existam acessos
            else:
                for item in resultados:
                    data = item["data_hora"]
                    data_formatada = data.strftime("%d/%m/%Y às %H:%M")
                    cod = item["codigo"]

                    # Cria card do acesso
                    card = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"Código usado: {cod}", size=16, weight=ft.FontWeight.BOLD, color="#28044C"),
                                ft.Text(data_formatada, size=14, color=ft.Colors.BLACK),
                            ],
                            spacing=5
                        ),
                        padding=15,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=5,
                            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                            offset=ft.Offset(0, 3)
                        ),
                        width=page.width,
                    )

                    lista_acessos.controls.append(card)

        except Exception as e:
            lista_acessos.controls.append(
                ft.Text(f"Erro ao carregar acessos: {e}", size=14, color="red")
            )

        page.update()

    # Retorna conteúdo + função
    return conteudo, carregar_ultimo_codigo
