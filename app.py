# app.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Projeto CIARTEC
#
# Este arquivo cuida apenas de:
#   1. configurar a página
#   2. carregar o CSS
#   3. mostrar a página (etapa) atual
#   4. mostrar os botões de navegação no final dela
#
# Não há sidebar: o leitor avança pelos botões no fim de cada página.
#
# Para rodar:  streamlit run app.py
# ==========================================================

from functools import partial
from pathlib import Path

import streamlit as st

from componentes import navegacao_paginas, rolar_para_o_topo, rodape
from dados import projeto, jornais
from paginas import pagina_jornal
from quiz import mostrar_quiz


# ==========================================================
# ETAPAS DO SITE (na ordem em que o leitor as percorre)
#
# Cada jornal de dados.py vira uma página, e a avaliação fecha o percurso.
# Para incluir outra página (por exemplo pagina_clima, de paginas.py),
# adicione uma linha na lista, na posição desejada:
#
#   {"funcao": pagina_clima, "proxima": "Texto do botão"}
# ==========================================================

ETAPAS = [
    {
        "funcao": partial(pagina_jornal, i),
        "proxima": jornal.get("proxima", "Próxima página")
    }
    for i, jornal in enumerate(jornais)
]

ETAPAS.append({"funcao": mostrar_quiz, "proxima": None})


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# (precisa ser o primeiro comando do Streamlit)
# ==========================================================

st.set_page_config(
    page_title=projeto["nome"],
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# CSS
# Toda a aparência está em estilo.css
# ==========================================================

def carregar_css():
    caminho = Path(__file__).parent / "estilo.css"
    css = caminho.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


carregar_css()


# ==========================================================
# PÁGINA ATUAL
# st.session_state["etapa"] guarda em que página o leitor está
# ==========================================================

if "etapa" not in st.session_state:
    st.session_state["etapa"] = 0

etapa = max(0, min(st.session_state["etapa"], len(ETAPAS) - 1))
st.session_state["etapa"] = etapa

ETAPAS[etapa]["funcao"]()


# ==========================================================
# BOTÕES NO FINAL DA PÁGINA + RODAPÉ
# ==========================================================

navegacao_paginas("etapa", len(ETAPAS), ETAPAS[etapa]["proxima"])

rodape(projeto["rodape"])

rolar_para_o_topo()
