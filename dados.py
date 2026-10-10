# dados.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Banco de informações do projeto
#
# Para alterar um TEXTO do site, edite este arquivo.
# Parágrafos dentro de """ """ são separados por uma linha em branco.
# ==========================================================


# ==========================================================
# PROJETO (nome, navegação e rodapé)
# ==========================================================

projeto = {
    "nome": "Ásia em Transformação",
    "jornal": "Jornal Voz Ativa",
    "edicao": "Edição especial",
    "descricao": (
        "Jornal digital do projeto CIARTEC sobre a Ásia em transformação: "
        "Afeganistão, desigualdade social e ODS 10."
    ),

    # QR code para abrir o jornal em outro dispositivo (aparece acima do rodapé).
    #   arquivo: coloque a imagem em imagens/ (aceita .png, .jpg, .webp e .svg).
    #            Enquanto ela não existir, o site mostra um espaço reservado.
    #   url:     endereço do site publicado; se preenchido, aparece escrito
    #            embaixo do QR code (para quem não conseguir escanear).
    "qrcode": {
        "arquivo": "qrcode.png",
        "url": "https://gomes333.github.io/projeto-ciartec/",
        "titulo": "Leia em outro dispositivo",
        "texto": "Aponte a câmera do celular ou do tablet para o QR code e abra este jornal na hora.",
    },

    "rodape": [
        "Ásia em Transformação",
        "Projeto desenvolvido para a CIARTEC",
        "Python • Jinja2 • HTML, CSS e JavaScript"
    ]
}


# ==========================================================
# PÁGINA INICIAL (jornais)
#
# Cada item da lista "jornais" é uma página de jornal.
# A ordem da lista é a ordem das páginas no menu do site.
# Cada jornal precisa de "slug" (nome do arquivo, sem .html) e "secao" (nome no menu).
#
# Estrutura de um jornal:
#   - cabeçalho: nome, titulo, editorias
#   - manchete:  chamada, manchete, linha_fina
#   - imagem_principal: foto grande abaixo da manchete
#   - colunas: lista de colunas; cada coluna é uma lista de blocos
#
# Tipos de bloco dentro de uma coluna:
#   {"titulo": "...", "subtitulo": "..."}   título da coluna (subtitulo é opcional)
#   {"texto": "..."}                        texto (linha em branco = novo parágrafo)
#   {"imagem": "arquivo.jpg", "descricao": "..."}   foto da pasta imagens/
#
# "descricao" é o texto alternativo da foto (acessibilidade).
# ==========================================================

jornais = [

    {
        "slug": "index",
        "secao": "Capa",
        "nome": "JORNAL VOZ ATIVA",
        "titulo": "O AFEGANISTÃO HOJE",
        "editorias": "POLÍTICA • ECONOMIA • SOCIEDADE • EDUCAÇÃO • DIREITOS HUMANOS",

        # Texto do botão no final desta página (a seta é adicionada sozinha)
        "proxima": "Continuar a leitura",

        "chamada": "AFEGANISTÃO: UM PAÍS DE CONTRASTES ENTRE",
        "manchete": "TRADIÇÕES, DESAFIOS E ESPERANÇA",
        "linha_fina": """
        Um país de história rica, marcado por conflitos,
        resistência e pela luta por um futuro melhor.
        """,

        "imagem_principal": {
            "arquivo": "afeganistao_montanhas.jpg",
            "descricao": "Montanhas com picos nevados e vale seco no Afeganistão"
        },

        "colunas": [

            # Coluna 1
            [
                {
                    "texto": """
                    Localizado na Ásia Central, o Afeganistão é um país de
                    grande importância histórica, cultural e geográfica. Com
                    paisagens impressionantes, como as montanhas do Hindu Kush,
                    o país também é marcado por anos de guerra, instabilidade
                    política e desafios sociais. Mesmo diante de tantas
                    dificuldades, o povo afegão continua resistente e busca
                    por melhores condições de vida, paz e direitos para todos.
                    """
                },
                {
                    "imagem": "afeganistao_coletiva.jpg",
                    "descricao": "Autoridade cercada por jornalistas, câmeras e microfones"
                }
            ],

            # Coluna 2
            [
                {
                    "titulo": "POLÍTICA",
                    "subtitulo": "O PODER EM MEIO À INSTABILIDADE"
                },
                {
                    "texto": """
                    O Afeganistão vive há décadas em um cenário de
                    instabilidade política. Em 2021, o grupo Talibã retomou o
                    poder após a retirada das tropas dos Estados Unidos,
                    encerrando um período de 20 anos de presença internacional
                    no país. Desde então, o governo do Talibã é reconhecido
                    apenas por poucos países, e a situação política continua
                    marcada por restrições e pelo controle rígido da população.
                    """
                }
            ],

            # Coluna 3
            [
                {
                    "titulo": "ECONOMIA",
                    "subtitulo": "UM PAÍS RICO EM RECURSOS, MAS COM POUCA PROSPERIDADE"
                },
                {
                    "imagem": "afeganistao_economia.jpg",
                    "descricao": "Mulher de burca azul caminhando com crianças em um assentamento"
                },
                {
                    "texto": """
                    O Afeganistão possui grandes reservas de minerais, como
                    lítio, cobre, ferro e terras raras, além de uma forte
                    produção agrícola, especialmente de frutas secas, trigo e
                    papoula (usada na produção de ópio). No entanto, a economia
                    do país é fragilizada por conflitos, falta de
                    infraestrutura, dependência de ajuda internacional e
                    dificuldades no comércio exterior. O desemprego é alto e
                    grande parte da população vive na pobreza.
                    """
                }
            ]
        ]
    },

    # ------------------------------------------------------
    # Página 2: jornal interno (layout "interna")
    #   - nome:      nome do jornal no cabeçalho
    #   - materias:  lista de reportagens. "largura": "total" ocupa a
    #                linha inteira; as demais ficam lado a lado, em pares.
    #                Cada uma aceita: titulo, subtitulo, texto, imagem,
    #                descricao (texto alternativo), legenda e citacao
    #   - faixa:     caixa larga com título e texto
    #   - fecho:     painel final com o nome do jornal e uma frase
    # ------------------------------------------------------
    {
        "layout": "interna",
        "slug": "reportagens",
        "secao": "Reportagens",
        # usados no quadro "Nesta edição" da capa
        "destaque": "Desigualdade de gênero, educacional e social",
        "resumo": "Mulheres lutam por direitos, meninas ficam fora da escola e famílias vivem em extrema vulnerabilidade.",
        "nome": "JORNAL VOZ ATIVA",
        "proxima": "Testar meus conhecimentos",

        "materias": [

            {
                "largura": "total",
                "titulo": "DESIGUALDADE DE GÊNERO",
                "subtitulo": "MULHERES AINDA LUTAM POR SEUS DIREITOS",
                "texto": """
                No Afeganistão, as mulheres enfrentam grandes restrições.
                Com o retorno do Talibã, o acesso à educação, ao trabalho
                e à vida pública foi drasticamente limitado. Muitas
                meninas não podem frequentar a escola após os 12 anos, o
                uso do véu é obrigatório e a presença feminina em espaços
                públicos é restrita.

                Apesar de tudo, há mulheres que resistem, como Malala
                Yousafzai, que se tornou um símbolo mundial da luta pelo
                direito à educação e pela igualdade.
                """,
                "imagem": "malala.jpg",
                "descricao": "Retrato de Malala Yousafzai com um véu claro sobre a cabeça",
                "legenda": """
                Malala Yousafzai, ativista paquistanesa e símbolo da luta
                pela educação das meninas.
                """,
                "citacao": {
                    "texto": "Um livro, uma caneta, uma criança e um professor podem mudar o mundo",
                    "autor": "Malala Yousafzai"
                }
            },

            {
                "titulo": "DESIGUALDADE EDUCACIONAL",
                "subtitulo": "O FUTURO DE MUITOS ESTÁ FORA DA ESCOLA",
                "texto": """
                O acesso à educação é um dos principais desafios sociais
                do país, e meninas e mulheres enfrentam as restrições mais
                graves. Sem poder estudar, perdem oportunidades de
                trabalho e de participação na vida pública, o que ajuda a
                manter a desigualdade de uma geração para a outra.
                """,
                "imagem": "sala_de_aula.jpg",
                "descricao": "Sala de aula com meninas de véu branco voltadas para a professora",
                "legenda": """
                Sala de aula no Afeganistão. Muitas meninas não podem mais
                frequentar a escola.
                """
            },

            {
                "titulo": "DESIGUALDADE SOCIAL",
                "subtitulo": "MUITOS VIVEM EM CONDIÇÕES DE EXTREMA VULNERABILIDADE",
                "texto": """
                A desigualdade social no Afeganistão é profunda. Grande
                parte da população vive em áreas rurais, com acesso
                limitado a serviços básicos, como saúde, saneamento e
                moradia. Famílias inteiras dependem da agricultura de
                subsistência e enfrentam insegurança alimentar. A guerra
                e a pobreza agravam ainda mais essa realidade,
                especialmente para crianças, mulheres e grupos
                minoritários.
                """,
                "imagem": "familia_rural.jpg",
                "descricao": "Crianças e adultos diante de tendas em um acampamento no deserto",
                "legenda": "Família afegã em uma região rural do país."
            }
        ],

        "faixa": {
            "titulo": "O TALIBÃ",
            "texto": """
            O Talibã é o grupo que retomou o poder no Afeganistão em 2021,
            após a retirada das tropas dos Estados Unidos, encerrando 20
            anos de presença internacional no país.

            Desde então, o governo é reconhecido por poucos países, e a
            vida da população, em especial a de mulheres e meninas, é
            marcada por restrições e pelo controle rígido.
            """
        },

        "fecho": {
            "nome": "JORNAL VOZ ATIVA",
            "frase": """
            O Afeganistão não é apenas um lugar de guerra, mas também de
            cultura, coragem e pessoas que sonham com um futuro melhor.
            """
        }
    }

    # Para adicionar outro jornal, copie um dos blocos { ... } acima,
    # coloque uma vírgula depois do }, e altere os textos e as imagens.
    # Cada item da lista vira uma página, na ordem em que aparece aqui.
]


# ==========================================================
# MUDANÇAS CLIMÁTICAS
# ==========================================================

clima = {
    "rotulo": "EIXO 01",
    "titulo": "Mudanças Climáticas na Ásia",
    "subtitulo": """
    Diferentes regiões do continente estão expostas
    a impactos ambientais distintos.
    """,

    "introducao": """
A Ásia é o maior continente do planeta e apresenta uma enorme
diversidade ambiental, econômica e populacional. Essa diversidade
também faz com que diferentes regiões estejam expostas a diferentes
impactos das mudanças climáticas.

O aumento das temperaturas, eventos extremos, alterações no regime
de chuvas, derretimento de geleiras, enchentes e períodos de seca
podem afetar diretamente a população, a agricultura, os recursos
hídricos e as atividades econômicas.
""",

    "problemas": [
        "Aumento das temperaturas",
        "Enchentes e inundações",
        "Derretimento de geleiras",
        "Ondas de calor",
        "Secas prolongadas",
        "Escassez de água",
        "Impactos na agricultura",
        "Elevação do nível do mar"
    ],

    "regioes": {
        "Sul da Ásia": """
        A região apresenta elevada exposição a ondas de calor,
        enchentes, alterações nas chuvas e eventos extremos.
        """,

        "Sudeste Asiático": """
        Áreas costeiras e grandes centros urbanos estão expostos
        à elevação do nível do mar, tempestades e inundações.
        """,

        "Ásia Central": """
        A escassez de água, a desertificação e as alterações nos
        padrões de precipitação representam importantes desafios.
        """,

        "Leste Asiático": """
        Grandes centros urbanos enfrentam ondas de calor,
        eventos extremos e riscos relacionados às áreas costeiras.
        """
    },

    "curiosidades": [
        "A Ásia abriga algumas das maiores cadeias montanhosas do mundo.",
        "Os Himalaias possuem importantes reservas de gelo e neve.",
        "Grande parte da população asiática vive em áreas urbanas e costeiras.",
        "A agricultura de diversos países asiáticos depende diretamente dos regimes de chuva."
    ]
}


# ==========================================================
# AFEGANISTÃO
# ==========================================================

afeganistao = {
    "rotulo": "EIXO 02",
    "titulo": "Desigualdade Social no Afeganistão",
    "subtitulo": """
    Aspectos sociais, econômicos e de gênero
    relacionados à desigualdade no país.
    """,

    "introducao": """
O Afeganistão está localizado na região da Ásia Central e enfrenta
uma série de desafios sociais, econômicos e humanitários.

A pobreza, as dificuldades de acesso à educação e à saúde,
as limitações de oportunidades econômicas e as desigualdades
de gênero estão entre os principais fatores relacionados
à desigualdade social no país.
""",

    "informacoes": {
        "Capital": "Cabul",
        "Continente": "Ásia",
        "Região": "Ásia Central",
        "Moeda": "Afegane"
    },

    "desigualdades": [
        {
            "titulo": "Educação",
            "texto": """
            O acesso à educação é um dos principais desafios sociais
            enfrentados no país. As meninas e mulheres enfrentam
            restrições particularmente graves nesse campo.
            """
        },

        {
            "titulo": "Desigualdade de gênero",
            "texto": """
            Mulheres e meninas enfrentam limitações significativas
            em áreas como educação, trabalho, participação social
            e autonomia.
            """
        },

        {
            "titulo": "Economia",
            "texto": """
            A pobreza e a falta de oportunidades econômicas afetam
            grande parte da população e contribuem para a manutenção
            das desigualdades sociais.
            """
        },

        {
            "titulo": "Saúde",
            "texto": """
            O acesso aos serviços de saúde pode ser limitado,
            principalmente para pessoas que vivem em áreas remotas
            ou em situação de vulnerabilidade.
            """
        }
    ],

    "grupos": [
        "Mulheres e meninas",
        "Crianças",
        "População rural",
        "Famílias em situação de pobreza",
        "Pessoas afetadas por conflitos e deslocamentos"
    ]
}


# ==========================================================
# ODS 10
# ==========================================================

ods10 = {
    "rotulo": "EIXO 03",
    "titulo": "ODS 10 — Redução das Desigualdades",
    "subtitulo": """
    Um dos Objetivos de Desenvolvimento Sustentável
    estabelecidos pela Organização das Nações Unidas.
    """,

    "introducao": """
A ODS 10 integra os Objetivos de Desenvolvimento Sustentável
estabelecidos pela Organização das Nações Unidas.

Seu propósito é reduzir as desigualdades dentro dos países
e entre diferentes países, promovendo inclusão social, econômica
e política.
""",

    "objetivos": [
        "Reduzir desigualdades sociais e econômicas.",
        "Promover inclusão social, econômica e política.",
        "Garantir oportunidades para diferentes grupos sociais.",
        "Combater discriminação e exclusão.",
        "Ampliar o acesso a oportunidades."
    ],

    # Duas caixas lado a lado (antes eram as chaves "afeganistao" e "clima")
    "conexoes": [
        {
            "rotulo": "APLICAÇÃO",
            "titulo": "ODS 10 e Afeganistão",
            "texto": """
A realidade do Afeganistão apresenta uma relação direta com
os objetivos da ODS 10.

As dificuldades de acesso à educação, ao trabalho, à saúde
e à participação social demonstram como determinados grupos
podem enfrentar obstáculos muito maiores para exercer seus
direitos e desenvolver suas oportunidades.
"""
        },
        {
            "rotulo": "CONEXÃO",
            "titulo": "Clima e desigualdade",
            "texto": """
As mudanças climáticas também possuem uma dimensão social.

Populações com menor acesso a recursos financeiros, infraestrutura
e serviços públicos geralmente apresentam maior dificuldade para
se adaptar a eventos climáticos extremos.

Por isso, mudanças climáticas e desigualdade social são problemas
que podem se reforçar mutuamente.
"""
        }
    ],

    "conclusao": {
        "rotulo": "CONCLUSÃO",
        "titulo": "Os desafios estão conectados",
        "texto": """
        Compreender as desigualdades sociais também significa
        compreender quem possui maior ou menor capacidade
        de enfrentar os impactos ambientais.
        """
    }
}


# ==========================================================
# DADOS PARA VISUALIZAÇÃO
# ==========================================================

impactos_climaticos = {
    "Problema": [
        "Ondas de calor",
        "Enchentes",
        "Secas",
        "Elevação do nível do mar",
        "Impactos na agricultura"
    ],

    "Nivel": [
        90,
        85,
        75,
        80,
        85
    ]
}

# Aviso exibido abaixo do gráfico (os valores acima são ilustrativos)
aviso_impactos = "Escala ilustrativa utilizada exclusivamente para visualização."