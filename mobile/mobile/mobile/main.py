import flet as ft
from pages.login_page import login_page
from pages.home_page import home_page
from pages.gerar_page import gerar_page
from pages.codigo_page import codigo_page

def main(page: ft.Page):
    page.title = "App Multi-página"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    pagina_atual = "login"
    dados_usuario = {
        "nome": "Estudante Flet",
        "nivel": "Iniciante",
        "pontos": 150,
        "configuracoes": {"modo_escuro": False, "notificacoes": True}
    }

    # --- define mudar_pagina primeiro ---
    def mudar_pagina(nova_pagina):
        nonlocal pagina_atual
        pagina_atual = nova_pagina
        for c in paginas:
            c.visible = False

        if pagina_atual in ["login", "codigo"]:
            barra_navegacao_container.visible = False
        else:
            barra_navegacao_container.visible = True # mostra a barra em todas as outras telas

        if pagina_atual == "login":
            conteudo_login.visible = True
            barra_navegacao_container.visible = False

        elif pagina_atual == "home":
            conteudo_home.visible = True

        elif pagina_atual == "gerar":
            conteudo_gerar.visible = True

        elif pagina_atual == "codigo":
            conteudo_codigo.visible = True

        atualizar_barra_navegacao()
        page.update()

    # --- depois carrega as páginas ---
    conteudo_login = login_page(page, mudar_pagina)
    conteudo_home, texto_pontos = home_page(dados_usuario, page, mudar_pagina)
    conteudo_gerar = gerar_page(dados_usuario, page=page, mudar_pagina=mudar_pagina)
    conteudo_codigo = codigo_page(page, mudar_pagina)

    paginas = [conteudo_login, conteudo_home, conteudo_gerar, conteudo_codigo]

    # --- Funções de navegação ---
    def ir_home(e): mudar_pagina("home")
    def ir_gerar(e): mudar_pagina("gerar")

    def criar_item_navegacao(icone, on_click_func):
        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Icon(icone, size=28, color=ft.Colors.BLACK),
                padding=ft.padding.all(10),
                border_radius=50,
                bgcolor=ft.Colors.TRANSPARENT
            ),
            on_tap=on_click_func
        )

    # --- Ícones da barra ---
    item_home = criar_item_navegacao(ft.Icons.HOME_OUTLINED, ir_home)
    item_gerar = criar_item_navegacao(ft.Icons.QR_CODE, ir_gerar)

    # --- Atualização do estado visual ---
    def atualizar_barra_navegacao():
        itens = [
            (item_home, "home"),
            (item_gerar, "gerar")
        ]
        for item, nome in itens:
            container = item.content
            icone = container.content
            if pagina_atual == nome:
                container.bgcolor = "#BDACE4"
                icone.color = "#28044C"
            else:
                container.bgcolor = ft.Colors.TRANSPARENT
                icone.color = ft.Colors.BLACK

    # --- Barra de navegação com fundo colorido (#E4D8FF) ---
    barra_navegacao = ft.Row(
        controls=[item_home, item_gerar],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    barra_navegacao_container = ft.Container(
        content=barra_navegacao,
        bgcolor="#E4D8FF",  # Fundo lilás claro
        padding=ft.padding.symmetric(vertical=12),
        border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.BLACK))),
        visible=False,
        
    )

    # --- Layout principal ---
    page.add(
        ft.Column(
            controls=[
                ft.Stack(controls=paginas),
                barra_navegacao_container  # Barra com fundo
            ],
            spacing=0,
            expand=True
        )
    )

ft.app(target=main, assets_dir="assets")

# INSTALADO pip install mysql-connector-python - Foi instalado isso no Flet porque ele é um aplicativo Python que se conecta **diretamente ao banco de dados MySQL**, e por isso precisa de um conector instalado localmente. No **Flask**, essa instalação **não foi necessária** porque o acesso ao banco já é feito **indiretamente pelo SQLAlchemy**, que usa internamente o conector do MySQL (como o `pymysql`) para gerenciar a conexão automaticamente.