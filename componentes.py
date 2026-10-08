# componentes.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Componentes visuais reutilizáveis
#
# Cada função aqui desenha um "pedaço" da interface.
# As cores e tamanhos NÃO ficam aqui: ficam em estilo.css.
# Os textos NÃO ficam aqui: ficam em dados.py.
# ==========================================================

import re

import streamlit as st

try:
    import streamlit.components.v1 as components
except Exception:  # pragma: no cover
    components = None


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def renderizar_html(html):
    """
    Mostra um bloco de HTML na tela.

    Por que isso existe?
    O Markdown (que o st.markdown usa por baixo) transforma linhas
    com 4 ou mais espaços de indentação, e blocos separados por
    linha em branco, em "código". Foi isso que fazia o HTML aparecer
    como texto na tela.

    Aqui juntamos tudo em uma única linha, sem indentação e sem
    linhas em branco, então isso não acontece mais.
    Use SEMPRE esta função em vez de st.markdown(..., unsafe_allow_html=True).
    """
    linhas = [linha.strip() for linha in html.splitlines() if linha.strip()]
    st.markdown(" ".join(linhas), unsafe_allow_html=True)


def paragrafos_html(texto, classe=""):
    """
    Transforma um texto de dados.py em parágrafos <p>.
    Uma linha em branco no texto separa um parágrafo do outro.
    """
    atributo = f' class="{classe}"' if classe else ""
    blocos = re.split(r"\n\s*\n", texto.strip())
    paragrafos = []

    for bloco in blocos:
        bloco_limpo = " ".join(bloco.split())
        if bloco_limpo:
            paragrafos.append(f"<p{atributo}>{bloco_limpo}</p>")

    return "".join(paragrafos)


def limpar(texto):
    """Remove quebras de linha e espaços extras de um texto."""
    return " ".join(texto.split())


# ==========================================================
# CABEÇALHOS E DESTAQUES
# ==========================================================

def hero(rotulo, titulo, texto, compacto=False):
    """Bloco grande escuro. Use compacto=True para a versão menor."""
    classe = "hero hero-compact" if compacto else "hero"

    renderizar_html(f"""
        <div class="{classe}">
            <div class="hero-content">
                <div class="hero-label">{rotulo}</div>
                <h1>{limpar(titulo)}</h1>
                <p>{limpar(texto)}</p>
            </div>
        </div>
    """)


def cabecalho_pagina(rotulo, titulo, texto):
    """Título no topo de cada página."""
    renderizar_html(f"""
        <div class="page-header">
            <div class="page-label">{rotulo}</div>
            <h1>{limpar(titulo)}</h1>
            <p>{limpar(texto)}</p>
        </div>
    """)


# ==========================================================
# CARDS E CAIXAS
# ==========================================================

def card(rotulo, titulo, texto):
    """Card com rótulo, título e texto (usado nos eixos do projeto)."""
    renderizar_html(f"""
        <div class="card">
            <div class="card-label">{rotulo}</div>
            <h3>{limpar(titulo)}</h3>
            <p>{limpar(texto)}</p>
        </div>
    """)


def item_lista(texto):
    """Card pequeno de uma linha (usado em listas de itens)."""
    renderizar_html(f'<div class="problem-card">{texto}</div>')


def caixa_info(texto, titulo=None):
    """Caixa azul clara com barra lateral. O título é opcional."""
    if titulo:
        conteudo = f"<strong>{titulo}</strong><br>{limpar(texto)}"
    else:
        conteudo = limpar(texto)

    renderizar_html(f'<div class="info-box">{conteudo}</div>')


def caixa_destaque(rotulo, titulo, texto):
    """Caixa branca com borda azul, para ideias centrais."""
    renderizar_html(f"""
        <div class="highlight-box">
            <div class="card-label">{rotulo}</div>
            <h2>{limpar(titulo)}</h2>
            {paragrafos_html(texto)}
        </div>
    """)


def grade_de_itens(itens, n_colunas=2):
    """Mostra uma lista de textos como cards pequenos, em colunas."""
    colunas = st.columns(n_colunas)

    for i, item in enumerate(itens):
        with colunas[i % n_colunas]:
            item_lista(item)


# ==========================================================
# CARROSSEL
# ==========================================================

def carrossel(itens, desenhar, chave="carrossel"):
    """
    Mostra um item por vez, com botões ANTERIOR e PRÓXIMA.

    itens:    lista com os itens (ex.: a lista "jornais" de dados.py)
    desenhar: função que recebe UM item e o mostra na tela
    chave:    nome único, só precisa mudar se houver 2 carrosséis na mesma página
    """
    if not itens:
        return

    total = len(itens)
    chave_indice = f"{chave}_indice"

    # st.session_state guarda o item atual entre um clique e outro
    if chave_indice not in st.session_state:
        st.session_state[chave_indice] = 0

    def voltar():
        st.session_state[chave_indice] -= 1

    def avancar():
        st.session_state[chave_indice] += 1

    indice = st.session_state[chave_indice]

    # A "key" permite ao estilo.css manter os 3 botões lado a lado no celular.
    # (Em versões antigas do Streamlit a key não existe; nesse caso não faz falta.)
    try:
        barra = st.container(key=f"carrossel-nav-{chave}")
    except TypeError:
        barra = st.container()

    with barra:

        col_voltar, col_indicador, col_avancar = st.columns(3)

        with col_voltar:
            st.button(
                "ANTERIOR",
                key=f"{chave}_voltar",
                on_click=voltar,
                disabled=(indice == 0)
            )

        with col_indicador:
            renderizar_html(
                f'<div class="carrossel-indicador">{indice + 1} / {total}</div>'
            )

        with col_avancar:
            st.button(
                "PRÓXIMA",
                key=f"{chave}_avancar",
                on_click=avancar,
                disabled=(indice == total - 1)
            )

    desenhar(itens[indice])


# ==========================================================
# SIDEBAR E RODAPÉ
# ==========================================================

def logo_sidebar(titulo, subtitulo):
    st.sidebar.markdown(
        f"""<div class="sidebar-logo"><h2>{titulo}</h2><p>{subtitulo}</p></div>""",
        unsafe_allow_html=True
    )


def secao_sidebar(texto):
    st.sidebar.markdown(
        f'<div class="sidebar-section">{texto}</div>',
        unsafe_allow_html=True
    )


def nota_sidebar(texto):
    st.sidebar.markdown(
        f'<div class="sidebar-note">{texto}</div>',
        unsafe_allow_html=True
    )


def rodape(linhas):
    """Rodapé com uma linha de texto por item da lista."""
    texto = "<br>".join(linhas)
    renderizar_html(f'<div class="footer">{texto}</div>')


def espaco():
    """Espaço vertical em branco (tamanho definido em estilo.css)."""
    renderizar_html('<div class="espaco"></div>')


# ==========================================================
# NAVEGAÇÃO ENTRE PÁGINAS (botões no fim de cada página)
# ==========================================================

def _container_com_chave(chave):
    """Container com "key" (a key permite ao estilo.css mirar nele)."""
    try:
        return st.container(key=chave)
    except TypeError:
        return st.container()


def navegacao_paginas(chave, total, texto_proxima=None):
    """
    Barra de navegação para o FINAL de cada página.

    chave:          nome em st.session_state que guarda a página atual (0, 1, 2...)
    total:          quantidade de páginas
    texto_proxima:  texto do botão de avançar (a seta é adicionada aqui)

    - Na primeira página não existe "Página anterior".
    - Na última página não existe botão de avançar.
    """
    atual = st.session_state[chave]

    def ir_para(destino):
        st.session_state[chave] = destino
        # pede para app.py rolar a tela para o topo da nova página
        st.session_state["rolar_pendente"] = True
        st.session_state["rolar_contagem"] = st.session_state.get("rolar_contagem", 0) + 1

    segmentos = "".join(
        '<span class="{}"></span>'.format(
            "feita" if i < atual else "atual" if i == atual else ""
        )
        for i in range(total)
    )

    renderizar_html(f"""
        <div class="nav-info">
            <div class="nav-progresso" aria-hidden="true">{segmentos}</div>
            <div class="nav-texto">Página {atual + 1} de {total}</div>
        </div>
    """)

    with _container_com_chave("nav-paginas"):

        col_voltar, col_avancar = st.columns([1, 1.8])

        with col_voltar:
            if atual > 0:
                st.button(
                    "← Página anterior",
                    key="nav-anterior",
                    on_click=ir_para,
                    args=(atual - 1,)
                )

        with col_avancar:
            if atual < total - 1:
                st.button(
                    f"{texto_proxima or 'Próxima página'} →",
                    key="nav-proxima",
                    on_click=ir_para,
                    args=(atual + 1,)
                )


def rolar_para_o_topo():
    """
    Depois de trocar de página, leva a tela de volta ao topo.
    Só age logo após um clique de navegação (não atrapalha o quiz).
    Chame no FINAL de app.py.
    """
    if not st.session_state.pop("rolar_pendente", False):
        return

    if components is None:
        return

    contagem = st.session_state.get("rolar_contagem", 0)

    with _container_com_chave("rolagem-topo"):
        # o número no comentário muda a cada clique, para o script rodar de novo
        components.html(
            f"""
            <script>
            // {contagem}
            function subir() {{
                var doc = window.parent.document;
                var alvos = [
                    doc.querySelector('[data-testid="stMain"]'),
                    doc.querySelector('section.main'),
                    doc.scrollingElement
                ];
                alvos.forEach(function (el) {{
                    if (el && el.scrollTo) {{ el.scrollTo(0, 0); }}
                }});
            }}
            subir();
            setTimeout(subir, 120);
            </script>
            """,
            height=0
        )
