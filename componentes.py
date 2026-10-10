# componentes.py
# ==========================================================
# ÁSIA EM TRANSFORMAÇÃO
# Funções auxiliares usadas pelos templates (filtros do Jinja2)
# e preparação das imagens.
#
#   - textos        -> dados.py / quiz.py
#   - estrutura     -> templates/*.html
#   - aparência     -> static/estilo.css
# ==========================================================

import re
import shutil
from datetime import date
from pathlib import Path

from markupsafe import Markup, escape

try:
    from PIL import Image
except ImportError:  # Pillow é opcional: sem ele as fotos são só copiadas
    Image = None


DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
        "sexta-feira", "sábado", "domingo"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

# Nomes próprios que mantêm a inicial maiúscula quando um título
# escrito em CAIXA ALTA é convertido para "Maiúscula só no início".
NOMES_PROPRIOS = [
    "Afeganistão", "Talibã", "Malala Yousafzai", "Malala", "Estados Unidos",
    "Ásia Central", "Ásia", "Cabul", "ODS", "ONU", "CIARTEC",
]

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".svg"}
LARGURA_MAXIMA = 1600


# ----------------------------------------------------------
# Textos
# ----------------------------------------------------------

def limpar(texto):
    """Remove quebras de linha e espaços extras."""
    return " ".join(str(texto).split())


def sentenca(texto):
    """'DESIGUALDADE DE GÊNERO' -> 'Desigualdade de gênero' (mantém nomes próprios)."""
    texto = limpar(texto).lower()
    texto = texto[:1].upper() + texto[1:]
    for nome in NOMES_PROPRIOS:
        texto = re.sub(rf"\b{re.escape(nome)}\b", nome, texto, flags=re.IGNORECASE)
    return texto


def nome_proprio(texto):
    """'JORNAL VOZ ATIVA' -> 'Jornal Voz Ativa'."""
    return limpar(texto).title()


def lista_editorias(texto):
    """'POLÍTICA • ECONOMIA' -> ['Política', 'Economia']."""
    return [sentenca(parte) for parte in texto.split("•") if parte.strip()]


def paragrafos(texto):
    """Uma linha em branco separa um parágrafo do outro. Devolve HTML seguro."""
    blocos = re.split(r"\n\s*\n", str(texto).strip())
    return Markup("".join(f"<p>{escape(limpar(b))}</p>" for b in blocos if b.strip()))


def tempo_leitura(jornal):
    """Estimativa em minutos (200 palavras por minuto), somando todos os textos."""
    def palavras(valor):
        if isinstance(valor, str):
            return len(valor.split())
        if isinstance(valor, dict):
            return sum(palavras(v) for k, v in valor.items() if k not in ("imagem", "descricao", "slug"))
        if isinstance(valor, (list, tuple)):
            return sum(palavras(v) for v in valor)
        return 0

    return max(1, round(palavras(jornal) / 200))


def data_por_extenso(d=None):
    d = d or date.today()
    return f"{DIAS[d.weekday()]}, {d.day} de {MESES[d.month - 1]} de {d.year}"


# ----------------------------------------------------------
# Imagens
# ----------------------------------------------------------

def preparar_imagens(origem: Path, destino: Path):
    """
    Copia as fotos de imagens/ para dist/imagens/, reduzindo as muito grandes
    (se o Pillow estiver instalado). Devolve a lista com os nomes reais encontrados.
    """
    encontradas = []
    destino.mkdir(parents=True, exist_ok=True)

    if not origem.exists():
        return encontradas

    for arquivo in sorted(origem.iterdir()):
        if arquivo.suffix.lower() not in EXTENSOES:
            continue

        encontradas.append(arquivo.name)
        saida = destino / arquivo.name

        # SVG (vetorial) e ausência do Pillow: copia sem mexer
        if Image is None or arquivo.suffix.lower() == ".svg":
            shutil.copy2(arquivo, saida)
            continue

        with Image.open(arquivo) as foto:
            if max(foto.size) <= LARGURA_MAXIMA:
                shutil.copy2(arquivo, saida)
                continue
            foto.thumbnail((LARGURA_MAXIMA, LARGURA_MAXIMA))
            if saida.suffix.lower() in (".jpg", ".jpeg"):
                foto.convert("RGB").save(saida, quality=84, optimize=True, progressive=True)
            else:
                foto.save(saida)

    return encontradas


def resolver_imagem(encontradas, nome):
    """
    Acha o arquivo real para o nome pedido em dados.py, tolerando diferenças que o
    Windows esconde: maiúsculas/minúsculas e extensão (.jpg, .JPG, .jpeg, .png, .webp).
    Devolve o nome real do arquivo ou None.
    """
    pedido = nome.lower()
    for real in encontradas:
        if real.lower() == pedido:
            return real
    base = Path(pedido).stem
    for real in encontradas:
        if Path(real).stem.lower() == base:
            return real
    return None
