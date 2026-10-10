# quiz.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Perguntas do desafio (quiz)
#
# Aqui ficam só os DADOS do quiz. A interação (feedback, placar,
# resultado, compartilhar) está em static/quiz.js e o visual em
# static/estilo.css. O build.py converte estas listas em JSON e
# embute na página quiz.html.
#
# Para ADICIONAR uma pergunta: copie um bloco { ... } de "perguntas".
#   - "resposta" precisa ser IDÊNTICA a uma das "opcoes".
#   - "explicacao" aparece como "Nota da redação" depois que o
#     leitor responde (certo ou errado).
# As alternativas são embaralhadas a cada tentativa.
# ==========================================================

import json

perguntas = [
    {
        "pergunta": "Qual é o principal objetivo da ODS 10?",
        "opcoes": [
            "Aumentar a produção industrial",
            "Reduzir as desigualdades",
            "Expandir territórios",
            "Aumentar o crescimento populacional",
        ],
        "resposta": "Reduzir as desigualdades",
        "explicacao": (
            "A ODS 10, da ONU, busca reduzir as desigualdades dentro dos países "
            "e entre eles, promovendo a inclusão social, econômica e política."
        ),
    },
    {
        "pergunta": "Qual país é analisado neste projeto em relação à desigualdade social?",
        "opcoes": ["Japão", "China", "Afeganistão", "Coreia do Sul"],
        "resposta": "Afeganistão",
        "explicacao": (
            "A capa e as reportagens da edição tratam do Afeganistão, na Ásia Central: "
            "desigualdade de gênero, educacional e social."
        ),
    },
    {
        "pergunta": "Qual fenômeno está relacionado às mudanças climáticas?",
        "opcoes": [
            "Derretimento de geleiras",
            "Redução permanente das temperaturas",
            "Diminuição dos eventos extremos",
            "Redução da radiação solar",
        ],
        "resposta": "Derretimento de geleiras",
        "explicacao": (
            "O aumento das temperaturas acelera o derretimento de geleiras, como as "
            "dos Himalaias, que abastecem rios dos quais milhões de pessoas dependem."
        ),
    },
    {
        "pergunta": "Qual grupo enfrenta importantes desigualdades no acesso à educação no Afeganistão?",
        "opcoes": ["Turistas", "Empresários", "Meninas e mulheres", "Atletas"],
        "resposta": "Meninas e mulheres",
        "explicacao": (
            "Desde o retorno do Talibã, em 2021, muitas meninas não podem frequentar "
            "a escola depois dos 12 anos. Sem estudar, perdem oportunidades de trabalho "
            "e de participação na vida pública."
        ),
    },
    {
        "pergunta": "Qual continente é analisado pelo projeto?",
        "opcoes": ["Europa", "África", "América", "Ásia"],
        "resposta": "Ásia",
        "explicacao": (
            "O projeto se chama Ásia em Transformação e parte do Afeganistão, "
            "país da Ásia Central, para discutir desigualdade e mudanças climáticas."
        ),
    },
    {
        "pergunta": "Qual dos seguintes fenômenos pode ser intensificado pelas mudanças climáticas?",
        "opcoes": [
            "Enchentes",
            "Redução de todos os conflitos",
            "Fim da urbanização",
            "Desaparecimento dos oceanos",
        ],
        "resposta": "Enchentes",
        "explicacao": (
            "Enchentes, secas e ondas de calor tendem a ficar mais intensas com o "
            "aquecimento global, e atingem mais quem tem menos recursos para se adaptar."
        ),
    },
]

# Mensagem final conforme o aproveitamento (de 0 a 1).
# O quiz.js usa a PRIMEIRA faixa cujo "minimo" foi atingido.
mensagens = [
    {
        "minimo": 1.0,
        "titulo": "Edição impecável",
        "texto": "Você dominou os principais conceitos apresentados.",
    },
    {
        "minimo": 0.5,
        "titulo": "Boa leitura",
        "texto": "Você compreendeu grande parte dos conceitos apresentados.",
    },
    {
        "minimo": 0.0,
        "titulo": "Vale reler a edição",
        "texto": "Alguns conceitos ainda podem ser revisados nas reportagens.",
    },
]


def validar():
    """Falha cedo (no build) se alguma resposta não estiver nas opções."""
    for n, p in enumerate(perguntas, start=1):
        if p["resposta"] not in p["opcoes"]:
            raise ValueError(f"Pergunta {n}: a resposta não é igual a nenhuma das opções.")
        if len(set(p["opcoes"])) != len(p["opcoes"]):
            raise ValueError(f"Pergunta {n}: há opções repetidas.")


def quiz_json():
    """JSON embutido na página do quiz."""
    validar()
    return json.dumps(
        {"perguntas": perguntas, "mensagens": mensagens},
        ensure_ascii=False,
    ).replace("</", "<\\/")
