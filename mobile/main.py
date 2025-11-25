import flet as ft
from pages.login_page import login_page
from pages.home_page import home_page
from pages.gerar_page import gerar_page
from pages.codigo_page import codigo_page
from pages.config_page import config_page
from pages.config_page import conectar
from pages.info_condominio_page import info_condominio_page
from pages.contatos_page import contatos_page
from pages.rec_facial_page import rec_facial_page
from pages.sobrenos_page import sobrenos_page

# Variável global para armazenar o morador logado
morador_logado_id = None

# Função para atualizar o morador logado
def set_morador_logado(valor):
    global morador_logado_id
    morador_logado_id = valor

# Função para retornar o morador logado
def get_morador_logado():
    return morador_logado_id

def main(page: ft.Page):
    page.title = "App Multi-página"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    pagina_atual = "login"

    # Função para mudar de página - mudar_pagina só altera visible dos containers.
    def mudar_pagina(nova_pagina):
        nonlocal pagina_atual
        pagina_atual = nova_pagina

        # Esconde todas as páginas
        for c in paginas:
            c.visible = False

        # Sempre ocultar cabeçalho extra
        cabecalho_info_condominio.visible = False
        cabecalho_contatos.visible = False
        cabecalho_rec_facial.visible = False
        cabecalho_sobrenos.visible = False

        # Cabeçalho e barra
        if pagina_atual == "login":
            cabecalho.visible = False
            barra_navegacao_container.visible = False
            conteudo_login.visible = True
        elif pagina_atual == "home":
            cabecalho.visible = True
            barra_navegacao_container.visible = True

            # --- BUSCAR nome do morador logado ---
            morador_id = get_morador_logado()
            nome = ""
            carregar_ultimo_codigo(morador_id)

            if morador_id:
                try:
                    conn = conectar()
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT nome_morador FROM moradores WHERE id = %s", (morador_id,))
                    row = cursor.fetchone()
                    if row:
                        nome = row["nome_morador"]
                    cursor.close()
                    conn.close()
                except:
                    nome = ""

            titulo_cabecalho.value = f"Bem-vindo(a), {nome}!" if nome else "Bem-vindo(a)!"

            conteudo_home.visible = True

        elif pagina_atual == "gerar":
            cabecalho.visible = True
            barra_navegacao_container.visible = True
            titulo_cabecalho.value = "Gerar código"
            conteudo_gerar.visible = True

        elif pagina_atual == "codigo":
            cabecalho.visible = False
            barra_navegacao_container.visible = False
            conteudo_codigo.visible = True

        elif pagina_atual == "config":
            cabecalho.visible = True
            barra_navegacao_container.visible = True
            titulo_cabecalho.value = "Configurações"
            conteudo_config.visible = True
            atualizar_config()

        elif pagina_atual == "info_condominio":
            cabecalho.visible = False
            cabecalho_info_condominio.visible = True
            barra_navegacao_container.visible = True
            conteudo_info_condominio.visible = True
        
        elif pagina_atual == "contatos":
            cabecalho.visible = False
            cabecalho_contatos.visible = True
            barra_navegacao_container.visible = True
            conteudo_contatos.visible = True

        elif pagina_atual == "rec_facial":
            cabecalho.visible = False
            cabecalho_rec_facial.visible = True
            barra_navegacao_container.visible = True
            conteudo_rec_facial.visible = True

        elif pagina_atual == "sobrenos":
            cabecalho.visible = False
            cabecalho_sobrenos.visible = True
            barra_navegacao_container.visible = True
            conteudo_sobrenos.visible = True

            atualizar_config() 

        atualizar_barra_navegacao()
        page.update()

    # Carregar todas as páginas
    conteudo_login = login_page(page, mudar_pagina, set_morador_logado)
    conteudo_home, carregar_ultimo_codigo = home_page(page, mudar_pagina)
    conteudo_gerar = gerar_page(page, mudar_pagina)
    conteudo_codigo = codigo_page(page, mudar_pagina, get_morador_logado)
    conteudo_config, atualizar_config = config_page(page, mudar_pagina, get_morador_logado)
    conteudo_info_condominio, cabecalho_info_condominio = info_condominio_page(page, mudar_pagina)
    conteudo_contatos, cabecalho_contatos = contatos_page(page, mudar_pagina)
    conteudo_rec_facial, cabecalho_rec_facial = rec_facial_page(page, mudar_pagina)
    conteudo_sobrenos, cabecalho_sobrenos = sobrenos_page(page, mudar_pagina)

    paginas = [conteudo_login, conteudo_home, conteudo_gerar, conteudo_codigo, conteudo_config, conteudo_info_condominio, conteudo_contatos, conteudo_rec_facial, conteudo_sobrenos]

    titulo_cabecalho = ft.Text(
        "",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#28044C",
    )

    # Cabeçalho simples
    cabecalho = ft.Container(
        content=ft.Container(
            content=titulo_cabecalho
        ),
        bgcolor="#E4D8FF",
        padding=20,
        alignment=ft.alignment.center,
        visible=False
    )

    # Função para criar item de navegação
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

    # Itens da barra de navegação
    def ir_home(e): mudar_pagina("home")
    def ir_gerar(e): mudar_pagina("gerar")
    def ir_config(e): mudar_pagina("config")

    item_home = criar_item_navegacao(ft.Icons.HOME_OUTLINED, ir_home)
    item_gerar = criar_item_navegacao(ft.Icons.QR_CODE_2, ir_gerar)
    item_config = criar_item_navegacao(ft.Icons.SETTINGS, ir_config)

    # Função para atualizar cores da barra
    def atualizar_barra_navegacao():
        itens = [(item_home, "home"), (item_gerar, "gerar"), (item_config, "config")]
        for item, nome in itens:
            container = item.content
            icone = container.content
            if pagina_atual == nome:
                container.bgcolor = "#BDACE4"
                icone.color = "#28044C"
            else:
                container.bgcolor = ft.Colors.TRANSPARENT
                icone.color = ft.Colors.BLACK

    # Barra de navegação
    barra_navegacao = ft.Row(
        controls=[item_home, item_gerar, item_config],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    barra_navegacao_container = ft.Container(
        content=barra_navegacao,
        bgcolor="#E4D8FF",
        padding=ft.padding.symmetric(vertical=12),
        border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.BLACK))),
        visible=False
    )

    # Adiciona tudo na tela
    page.add(
        ft.Column(
            controls=[cabecalho, cabecalho_info_condominio, cabecalho_contatos, cabecalho_rec_facial, cabecalho_sobrenos, ft.Stack(controls=paginas), barra_navegacao_container],
            spacing=0,
            expand=True
        )
    )

# Executa app
ft.app(target=main, assets_dir="assets")

# pip install mysql-connector-python
# Foi instalado isso no Flet porque ele é um aplicativo Python que se conecta **diretamente ao banco de dados MySQL**