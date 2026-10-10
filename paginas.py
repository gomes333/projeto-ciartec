# paginas.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Páginas do site (uma função por página)
#
# Aqui só montamos a página, juntando componentes e dados:
#   - o que aparece        -> dados.py
#   - como cada bloco é    -> componentes.py
#   - cores e tamanhos     -> estilo.css
# ==========================================================

import pandas as pd
import streamlit as st

from componentes import (
    hero,
    cabecalho_pagina,
    caixa_info,
    caixa_destaque,
    item_lista,
    grade_de_itens
)

from jornal import mostrar_jornal

from dados import (
    jornais,
    clima,
    afeganistao,
    ods10,
    impactos_climaticos,
    aviso_impactos
)


# ==========================================================
# PÁGINAS DE JORNAL
# Cada item da lista "jornais" (dados.py) é uma página do site.
# ==========================================================

def pagina_jornal(indice):

    mostrar_jornal(jornais[indice])


# ==========================================================
# MUDANÇAS CLIMÁTICAS
# ==========================================================

def pagina_clima():

    cabecalho_pagina(
        clima["rotulo"],
        clima["titulo"],
        clima["subtitulo"]
    )

    st.write(clima["introducao"])

    st.divider()

    st.subheader("Principais impactos")
    grade_de_itens(clima["problemas"])

    st.divider()

    st.subheader("Impactos por região")

    for regiao, descricao in clima["regioes"].items():
        with st.expander(regiao):
            st.write(descricao)

    st.divider()

    st.subheader("Visualização dos impactos")

    tabela = pd.DataFrame(impactos_climaticos)
    st.bar_chart(tabela.set_index("Problema"))
    st.caption(aviso_impactos)

    st.divider()

    st.subheader("Informações complementares")

    for curiosidade in clima["curiosidades"]:
        caixa_info(curiosidade)


# ==========================================================
# AFEGANISTÃO
# ==========================================================

def pagina_afeganistao():

    cabecalho_pagina(
        afeganistao["rotulo"],
        afeganistao["titulo"],
        afeganistao["subtitulo"]
    )

    st.write(afeganistao["introducao"])

    st.divider()

    st.subheader("Informações gerais")

    informacoes = afeganistao["informacoes"]
    colunas = st.columns(len(informacoes))

    for coluna, (nome, valor) in zip(colunas, informacoes.items()):
        coluna.metric(nome, valor)

    st.divider()

    st.subheader("Dimensões da desigualdade")

    for item in afeganistao["desigualdades"]:
        with st.expander(item["titulo"]):
            st.write(item["texto"])

    st.divider()

    st.subheader("Grupos em situação de maior vulnerabilidade")
    grade_de_itens(afeganistao["grupos"])


# ==========================================================
# ODS 10
# ==========================================================

def pagina_ods10():

    cabecalho_pagina(
        ods10["rotulo"],
        ods10["titulo"],
        ods10["subtitulo"]
    )

    st.write(ods10["introducao"])

    st.divider()

    st.subheader("Principais objetivos")

    for objetivo in ods10["objetivos"]:
        item_lista(objetivo)

    st.divider()

    # Uma caixa de destaque em cada coluna
    colunas = st.columns(len(ods10["conexoes"]))

    for coluna, conexao in zip(colunas, ods10["conexoes"]):
        with coluna:
            caixa_destaque(**conexao)

    st.divider()

    hero(**ods10["conclusao"], compacto=True)