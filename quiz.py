# quiz.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Sistema de avaliação interativa
#
# Para ADICIONAR uma pergunta: copie um bloco { ... } da lista
# "perguntas" abaixo e altere o texto. A "resposta" precisa ser
# idêntica a uma das "opcoes".
# ==========================================================

import streamlit as st

from componentes import cabecalho_pagina, caixa_info, renderizar_html, espaco


# ==========================================================
# PERGUNTAS
# ==========================================================

perguntas = [

    {
        "pergunta": "Qual é o principal objetivo da ODS 10?",
        "opcoes": [
            "Aumentar a produção industrial",
            "Reduzir as desigualdades",
            "Expandir territórios",
            "Aumentar o crescimento populacional"
        ],
        "resposta": "Reduzir as desigualdades"
    },

    {
        "pergunta": "Qual país é analisado neste projeto em relação à desigualdade social?",
        "opcoes": [
            "Japão",
            "China",
            "Afeganistão",
            "Coreia do Sul"
        ],
        "resposta": "Afeganistão"
    },

    {
        "pergunta": "Qual fenômeno está relacionado às mudanças climáticas?",
        "opcoes": [
            "Derretimento de geleiras",
            "Redução permanente das temperaturas",
            "Diminuição dos eventos extremos",
            "Redução da radiação solar"
        ],
        "resposta": "Derretimento de geleiras"
    },

    {
        "pergunta": "Qual grupo enfrenta importantes desigualdades no acesso à educação no Afeganistão?",
        "opcoes": [
            "Turistas",
            "Empresários",
            "Meninas e mulheres",
            "Atletas"
        ],
        "resposta": "Meninas e mulheres"
    },

    {
        "pergunta": "Qual continente é analisado pelo projeto?",
        "opcoes": [
            "Europa",
            "África",
            "América",
            "Ásia"
        ],
        "resposta": "Ásia"
    },

    {
        "pergunta": "Qual dos seguintes fenômenos pode ser intensificado pelas mudanças climáticas?",
        "opcoes": [
            "Enchentes",
            "Redução de todos os conflitos",
            "Fim da urbanização",
            "Desaparecimento dos oceanos"
        ],
        "resposta": "Enchentes"
    }
]


# ==========================================================
# LÓGICA DA AVALIAÇÃO
# ==========================================================

def calcular_pontuacao(respostas):
    """Recebe a lista de respostas do usuário e retorna quantas estão certas."""
    pontos = 0

    for pergunta, resposta in zip(perguntas, respostas):
        if resposta == pergunta["resposta"]:
            pontos += 1

    return pontos


def mostrar_mensagem_final(pontos, total):
    """Mostra um comentário de acordo com o desempenho."""
    if pontos == total:
        st.success(
            "Excelente desempenho. Você demonstrou domínio dos principais conceitos apresentados."
        )

    elif pontos >= total / 2:
        st.info(
            "Bom desempenho. Você compreendeu grande parte dos conceitos apresentados."
        )

    else:
        st.warning(
            "O resultado indica que alguns conceitos ainda podem ser revisados."
        )


# ==========================================================
# TELA DO QUIZ
# ==========================================================

def mostrar_quiz():

    cabecalho_pagina(
        "AVALIAÇÃO INTERATIVA",
        "Teste seus conhecimentos",
        """
        Responda às questões para verificar sua compreensão
        dos temas apresentados no projeto.
        """
    )

    caixa_info(
        titulo="Como funciona?",
        texto="""
        Selecione uma alternativa para cada questão e,
        ao final, confira seu desempenho.
        """
    )

    # Mostra as perguntas e guarda a resposta escolhida em cada uma
    respostas = []

    for i, pergunta in enumerate(perguntas):

        renderizar_html(f'<div class="question-number">QUESTÃO {i + 1}</div>')

        resposta = st.radio(
            pergunta["pergunta"],
            pergunta["opcoes"],
            key=f"pergunta_{i}"
        )

        respostas.append(resposta)

        espaco()

    # Calcula e mostra o resultado
    if st.button("FINALIZAR AVALIAÇÃO", use_container_width=True):

        pontos = calcular_pontuacao(respostas)
        total = len(perguntas)
        porcentagem = (pontos / total) * 100

        st.divider()

        renderizar_html('<div class="result-title">RESULTADO</div>')

        col1, col2 = st.columns(2)

        col1.metric("Questões corretas", f"{pontos}/{total}")
        col2.metric("Aproveitamento", f"{porcentagem:.0f}%")

        mostrar_mensagem_final(pontos, total)
