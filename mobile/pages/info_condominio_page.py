import flet as ft

def info_condominio_page(page, mudar_pagina):
    
    def voltar(e):
        mudar_pagina("config")

    # Cabeçalho
    titulo = ft.Text(
        "Informações do condomínio",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="black"
    )

    cabecalho = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_size=26,
                    icon_color="black",
                    on_click=voltar
                ),
                titulo
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor="#E4D8FF",
        padding=20,
        alignment=ft.alignment.center_left,
        visible=False
    )

    # ---------- ESTILOS ----------

    def card_titulo(texto):
        return ft.Text(texto, size=18, weight=ft.FontWeight.BOLD, color="black")

    def card_conteudo(texto):
        return ft.Text(texto, size=16, color="black")

    def card(conteudo):
        return ft.Container(
            content=conteudo,
            padding=20,
            width=page.width * 0.9,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
        )

    # ---------- CONTEÚDOS ----------

    dados_gerais = card(
        ft.Column([
            card_titulo("Dados gerais"),
            card_conteudo("Nome: Residencial Jardim das Flores"),
            card_conteudo("Endereço: Rua Primavera, nº 220 – Santo André/SP"),
            card_conteudo("Blocos: 3"),
        ], spacing=6)
    )

    regras_importantes = card(
        ft.Column([
            card_titulo("Regras importantes"),
            card_conteudo("• Horário do lixo: 18h – 22h"),
            card_conteudo("• Mudanças: 8h às 18h (seg–sáb)"),
            card_conteudo("• Garagem: apenas veículos cadastrados"),
            card_conteudo("• Silêncio: 22h – 6h"),
            card_conteudo("• Pets: somente com guia"),
        ], spacing=6)
    )

    areas_comuns = card(
        ft.Column([
            card_titulo("Áreas comuns"),
            card_conteudo("• Piscina até 20h"),
            card_conteudo("• Academia 6h – 22h"),
            card_conteudo("• Salão de festas: reservar 30 dias antes"),
            card_conteudo("• Playground"),
            card_conteudo("• Quadra poliesportiva"),
            card_conteudo("• Churrasqueiras"),
        ], spacing=6)
    )

    documentos = card(
        ft.Column([
            card_titulo("Documentos"),
            card_conteudo("• Regulamento interno"),
            card_conteudo("• Manual do morador"),
            card_conteudo("• Normas de convivência"),
        ], spacing=6)
    )

    # Conteúdo final
    conteudo = ft.Container(
        content=ft.Column(
            controls=[
                dados_gerais,
                regras_importantes,
                areas_comuns,
                documentos,
            ],
            spacing=25,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=20,
        visible=False
    )

    return conteudo, cabecalho
