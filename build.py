#!/usr/bin/env python3
# build.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO — gerador do site (substitui o antigo app.py)
#
# Lê os textos de dados.py e quiz.py, aplica os templates de
# templates/ e escreve o site pronto na pasta dist/.
# O resultado é HTML estático: abre em qualquer navegador e
# pode ser hospedado de graça (GitHub Pages, Netlify, Vercel).
#
# Uso:
#   python build.py            gera a pasta dist/
#   python build.py --serve    gera e abre em http://localhost:8000
#   python build.py --serve 9000   (porta diferente)
# ==========================================================

import argparse
import functools
import http.server
import shutil
import socketserver
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

import componentes as c
from dados import jornais, projeto
from quiz import quiz_json

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "dist"


def montar_paginas():
    """Cada jornal de dados.py vira uma página; o quiz fecha o percurso."""
    paginas = []

    for jornal in jornais:
        paginas.append({
            "arquivo": f'{jornal["slug"]}.html',
            "secao": jornal["secao"],
            "titulo": jornal.get("destaque") or c.sentenca(jornal["secao"]),
            "modelo": "interna.html" if jornal.get("layout") == "interna" else "capa.html",
            "jornal": jornal,
            "proxima": jornal.get("proxima", "Próxima página"),
            "resumo": jornal.get("resumo") or c.sentenca(jornal.get("manchete", "")),
        })

    paginas.append({
        "arquivo": "quiz.html",
        "secao": "Quiz",
        "titulo": "Teste seus conhecimentos",
        "modelo": "quiz.html",
        "jornal": None,
        "proxima": None,
        "resumo": "Seis perguntas para testar o que você leu nesta edição.",
    })

    return paginas


def criar_ambiente():
    env = Environment(
        loader=FileSystemLoader(RAIZ / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters.update({
        "sentenca": c.sentenca,
        "nome_proprio": c.nome_proprio,
        "paragrafos": c.paragrafos,
        "editorias": c.lista_editorias,
        "limpar": c.limpar,
    })
    env.globals["tempo_leitura"] = c.tempo_leitura
    return env


def limpar_saida():
    """
    Esvazia dist/ item por item. No Windows (principalmente em pastas do OneDrive)
    uma pasta em uso pode recusar a exclusão; nesse caso ela é ignorada e os
    arquivos são simplesmente sobrescritos pelo build.
    """
    SAIDA.mkdir(exist_ok=True)
    for item in SAIDA.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except OSError:
            pass


def gerar():
    limpar_saida()

    shutil.copytree(RAIZ / "static", SAIDA / "static", dirs_exist_ok=True)
    fotos = c.preparar_imagens(RAIZ / "imagens", SAIDA / "imagens")

    env = criar_ambiente()
    # global: fica visível também dentro dos macros (templates/macros.html)
    env.globals["foto_arquivo"] = lambda nome: c.resolver_imagem(fotos, nome)
    paginas = montar_paginas()
    quiz = quiz_json()

    contexto_base = {
        "projeto": projeto,
        "paginas": paginas,
        "hoje": c.data_por_extenso(),
        "quiz_json": quiz,
    }

    for i, pagina in enumerate(paginas):
        html = env.get_template(pagina["modelo"]).render(
            **contexto_base,
            pagina=pagina,
            indice=i,
            anterior=paginas[i - 1] if i > 0 else None,
            seguinte=paginas[i + 1] if i < len(paginas) - 1 else None,
            jornal=pagina["jornal"],
        )
        (SAIDA / pagina["arquivo"]).write_text(html, encoding="utf-8")

    html_404 = env.get_template("404.html").render(**contexto_base, pagina=None, indice=-1)
    (SAIDA / "404.html").write_text(html_404, encoding="utf-8")

    faltando = sorted({
        nome for nome in _fotos_usadas() if not c.resolver_imagem(fotos, nome)
    })
    print(f"Site gerado em {SAIDA}  ({len(paginas)} páginas)")
    if faltando:
        print("Atenção: estas fotos não estão em imagens/ (aparecem como espaço reservado):")
        for nome in faltando:
            print(f"  - {nome}")
        print("Arquivos encontrados em imagens/:", ", ".join(fotos) or "(nenhum)")
        print("Confira se os nomes batem (cuidado com extensão escondida, ex.: malala.jpg.jpg).")


def _fotos_usadas():
    for jornal in jornais:
        principal = jornal.get("imagem_principal")
        if principal:
            yield principal["arquivo"]
        for coluna in jornal.get("colunas", []):
            for bloco in coluna:
                if "imagem" in bloco:
                    yield bloco["imagem"]
        for materia in jornal.get("materias", []):
            if materia.get("imagem"):
                yield materia["imagem"]


def servir(porta):
    gerador = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SAIDA))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", porta), gerador) as servidor:
        print(f"Abra http://localhost:{porta}  (Ctrl+C para parar)")
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")


if __name__ == "__main__":
    analisador = argparse.ArgumentParser(description="Gera o site do Jornal Voz Ativa.")
    analisador.add_argument("--serve", nargs="?", const=8000, type=int, metavar="PORTA",
                            help="depois de gerar, serve o site localmente")
    argumentos = analisador.parse_args()

    gerar()
    if argumentos.serve:
        servir(argumentos.serve)
