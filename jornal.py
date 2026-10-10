# jornal.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Páginas de jornal em HTML/CSS
#
# Este arquivo só MONTA o HTML a partir dos dados de dados.py.
#   - o que está escrito  -> dados.py  (lista "jornais")
#   - como parece         -> estilo.css (seção "JORNAL")
#
# Existem dois modelos de página:
#   - capa    (padrão): manchete, foto principal e 3 colunas
#   - interna ("layout": "interna"): reportagens em grade, citações,
#                                    faixa e painel final
# ==========================================================

import base64
import io
from html import escape
from pathlib import Path

import streamlit as st
from PIL import Image

from componentes import renderizar_html, paragrafos_html, limpar


# Pasta onde ficam as fotos (ao lado deste arquivo)
PASTA_IMAGENS = Path(__file__).parent / "imagens"

# Largura máxima das fotos depois de reduzidas (em pixels)
LARGURA_FOTO_PRINCIPAL = 1400
LARGURA_FOTO_COLUNA = 900


# ==========================================================
# FOTOS
# ==========================================================

@st.cache_data(show_spinner=False)
def codificar_foto(caminho, modificado_em, largura_maxima):
    """
    Lê a foto, reduz e devolve em base64 para ser colocada dentro do HTML.

    O Streamlit não serve arquivos locais dentro de HTML, por isso a foto
    vai "embutida" no próprio código da página.
    O resultado fica em cache: a foto só é processada de novo se o
    arquivo mudar (por isso o parâmetro modificado_em).
    """
    foto = Image.open(caminho).convert("RGB")
    foto.thumbnail((largura_maxima, largura_maxima))

    memoria = io.BytesIO()
    foto.save(memoria, format="JPEG", quality=82, optimize=True)

    return base64.b64encode(memoria.getvalue()).decode("ascii")


def foto_html(arquivo, descricao, tamanho):
    """
    HTML de uma foto. tamanho: "larga" (foto principal) ou "media" (colunas).
    Se o arquivo não existir, mostra uma caixa cinza avisando o nome esperado.
    """
    caminho = PASTA_IMAGENS / arquivo
    classes = f"jornal-foto jornal-foto-{tamanho}"

    if not caminho.exists():
        return (
            f'<figure class="{classes} jornal-foto-vazia">'
            f'<span>Imagem não encontrada:<br>imagens/{escape(arquivo)}</span>'
            f'</figure>'
        )

    largura = LARGURA_FOTO_PRINCIPAL if tamanho == "larga" else LARGURA_FOTO_COLUNA
    foto64 = codificar_foto(str(caminho), caminho.stat().st_mtime, largura)

    return (
        f'<figure class="{classes}">'
        f'<img src="data:image/jpeg;base64,{foto64}" alt="{escape(descricao, quote=True)}">'
        f'</figure>'
    )


# ==========================================================
# BLOCOS DE UMA COLUNA
# ==========================================================

def bloco_html(bloco):
    """Transforma um bloco de dados.py (título, texto ou imagem) em HTML."""

    if "titulo" in bloco:
        html = f'<div class="jornal-titulo-coluna">{limpar(bloco["titulo"])}</div>'

        if bloco.get("subtitulo"):
            html += f'<div class="jornal-subtitulo-coluna">{limpar(bloco["subtitulo"])}</div>'

        return html

    if "texto" in bloco:
        return paragrafos_html(bloco["texto"], classe="jornal-texto")

    if "imagem" in bloco:
        return foto_html(bloco["imagem"], bloco.get("descricao", ""), "media")

    return ""


def coluna_html(blocos):
    conteudo = "".join(bloco_html(bloco) for bloco in blocos)
    return f'<div class="jornal-coluna">{conteudo}</div>'


# ==========================================================
# PEÇAS COMPARTILHADAS
# ==========================================================

def topo_html(nome):
    """Faixa do topo: nome do jornal, ornamento, nome do jornal."""
    nome = limpar(nome)

    return (
        '<div class="jornal-topo">'
        f'<div class="jornal-nome">{nome}</div>'
        '<div class="jornal-ornamento"><div class="jornal-losango"></div></div>'
        f'<div class="jornal-nome">{nome}</div>'
        '</div>'
    )


# ==========================================================
# PÁGINA INTERNA (reportagens, citações, faixa e painel final)
# ==========================================================

def quadro_html(arquivo, descricao, legenda=""):
    """Foto com legenda em caixa escura, usada nas reportagens."""
    caminho = PASTA_IMAGENS / arquivo

    if caminho.exists():
        foto64 = codificar_foto(
            str(caminho), caminho.stat().st_mtime, LARGURA_FOTO_COLUNA
        )
        miolo = (
            f'<img src="data:image/jpeg;base64,{foto64}" '
            f'alt="{escape(descricao, quote=True)}">'
        )
        classes = "jornal-quadro-foto"
    else:
        miolo = f'<span>Imagem não encontrada:<br>imagens/{escape(arquivo)}</span>'
        classes = "jornal-quadro-foto jornal-foto-vazia"

    texto_legenda = ""
    if legenda:
        texto_legenda = f'<figcaption class="jornal-legenda">{limpar(legenda)}</figcaption>'

    return (
        '<figure class="jornal-quadro">'
        f'<div class="{classes}">{miolo}</div>'
        f'{texto_legenda}'
        '</figure>'
    )


def citacao_html(citacao):
    return (
        '<blockquote class="jornal-citacao">'
        f'<p>“{limpar(citacao["texto"])}”</p>'
        f'<cite>{limpar(citacao["autor"])}</cite>'
        '</blockquote>'
    )


def materia_html(materia):
    """Uma reportagem: foto, título, subtítulo, texto e (opcional) citação."""
    larga = materia.get("largura") == "total"
    classes = "jornal-materia jornal-materia-larga" if larga else "jornal-materia"

    foto = ""
    if materia.get("imagem"):
        foto = quadro_html(
            materia["imagem"],
            materia.get("descricao", ""),
            materia.get("legenda", "")
        )

    subtitulo = ""
    if materia.get("subtitulo"):
        subtitulo = f'<div class="jornal-subtitulo-coluna">{limpar(materia["subtitulo"])}</div>'

    corpo = (
        '<div class="jornal-materia-corpo">'
        f'<div class="jornal-titulo-coluna">{limpar(materia["titulo"])}</div>'
        f'{subtitulo}'
        f'{paragrafos_html(materia["texto"], classe="jornal-texto")}'
        '</div>'
    )

    citacao = citacao_html(materia["citacao"]) if materia.get("citacao") else ""

    return f'<article class="{classes}">{foto}{corpo}{citacao}</article>'


def materias_html(materias):
    """
    Reportagens com "largura": "total" ocupam a linha inteira.
    As outras, em sequência, ficam lado a lado em pares.
    """
    partes = []
    par = []

    def fechar_par():
        if par:
            partes.append(f'<div class="jornal-par">{"".join(par)}</div>')
            par.clear()

    for materia in materias:
        html = materia_html(materia)

        if materia.get("largura") == "total":
            fechar_par()
            partes.append(html)
        else:
            par.append(html)

    fechar_par()
    return "".join(partes)


def faixa_html(faixa):
    return (
        '<aside class="jornal-faixa">'
        f'<div class="jornal-titulo-coluna">{limpar(faixa["titulo"])}</div>'
        f'<div>{paragrafos_html(faixa["texto"], classe="jornal-texto")}</div>'
        '</aside>'
    )


def fecho_html(fecho):
    # o espaço é mantido: no celular a quebra <br> some e as palavras ficam na mesma linha
    nome = limpar(fecho["nome"]).replace(" ", " <br>")

    return (
        '<aside class="jornal-fecho">'
        f'<div class="jornal-fecho-nome">{nome}</div>'
        f'<blockquote class="jornal-fecho-frase"><p>“{limpar(fecho["frase"])}”</p></blockquote>'
        '</aside>'
    )


def mostrar_jornal_interno(jornal):
    """Mostra uma página interna de jornal."""
    topo = topo_html(jornal["nome"])
    materias = materias_html(jornal["materias"])
    faixa = faixa_html(jornal["faixa"]) if jornal.get("faixa") else ""
    fecho = fecho_html(jornal["fecho"]) if jornal.get("fecho") else ""

    renderizar_html(f"""
        <div class="jornal jornal-interno" lang="pt-BR">
            <div class="jornal-papel">
                {topo}
                <div class="jornal-grade">{materias}{faixa}{fecho}</div>
            </div>
        </div>
    """)


# ==========================================================
# PÁGINA DE JORNAL (capa)
# ==========================================================

def mostrar_jornal(jornal):
    """Mostra uma página de jornal completa na tela."""

    if jornal.get("layout") == "interna":
        mostrar_jornal_interno(jornal)
        return

    principal = jornal["imagem_principal"]

    foto_principal = foto_html(
        principal["arquivo"],
        principal.get("descricao", ""),
        "larga"
    )

    colunas = "".join(coluna_html(coluna) for coluna in jornal["colunas"])
    topo = topo_html(jornal["nome"])

    renderizar_html(f"""
        <div class="jornal" lang="pt-BR">
            <div class="jornal-papel">

                {topo}

                <div class="jornal-titulo">{limpar(jornal["titulo"])}</div>
                <div class="jornal-editorias">{limpar(jornal["editorias"])}</div>

                <div class="jornal-chamada">{limpar(jornal["chamada"])}</div>
                <div class="jornal-manchete">{limpar(jornal["manchete"])}</div>
                <p class="jornal-linha-fina">{limpar(jornal["linha_fina"])}</p>

                {foto_principal}

                <div class="jornal-colunas">{colunas}</div>

            </div>
        </div>
    """)
