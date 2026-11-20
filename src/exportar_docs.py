"""Exporta documentos Markdown de docs/ a .docx y .pdf.

Uso (desde la raíz del proyecto):
    python src/exportar_docs.py docs/negocio.md [docs/tecnico.md ...]

- .docx: pandoc (incluido en el paquete `pypandoc_binary`, no requiere instalación).
- .pdf : si hay xelatex en el PATH se usa `--pdf-engine=xelatex`; si no, se genera
         HTML con estilo y se imprime a PDF con un navegador Chromium (Edge, Chrome o
         Chromium) en modo headless. Funciona en Windows, macOS y Linux.
"""
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pypandoc

CSS = """
@page { size: Letter; margin: 2.2cm 2cm; }
body { font-family: 'Calibri', 'Segoe UI', sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }
header#title-block-header { text-align: center; padding-top: 6cm; page-break-after: always; }
h1.title { font-size: 22pt; margin-bottom: .4em; }
p.subtitle { font-style: italic; color: #444; margin: 0 0 3em; font-size: 13pt; text-align: center; }
p.author { text-align: center; margin: .25em 0; font-size: 12pt; }
p.date { text-align: center; margin-top: 3em; color: #444; }
h2 { font-size: 13.5pt; border-bottom: 1px solid #999; padding-bottom: 2px; margin-top: 1.4em; }
h3 { font-size: 11.5pt; margin-top: 1.1em; }
p { text-align: justify; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: .8em 0; page-break-inside: auto; }
th, td { border: 1px solid #bbb; padding: 3px 5px; vertical-align: top; text-align: left; }
th { background: #e9eef4; }
tr { page-break-inside: avoid; }
code { font-family: Consolas, monospace; font-size: 9pt; }
"""

# Navegadores basados en Chromium que pueden imprimir HTML a PDF en modo headless,
# en el orden en que se buscan (Windows, macOS y Linux).
NAVEGADORES_RUTAS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
NAVEGADORES_PATH = ["microsoft-edge", "microsoft-edge-stable", "google-chrome", "google-chrome-stable",
                    "chromium", "chromium-browser"]


def buscar_navegador() -> str | None:
    """Ruta del primer navegador Chromium disponible (Edge, Chrome o Chromium), o None."""
    for ruta in NAVEGADORES_RUTAS:
        if Path(ruta).exists():
            return ruta
    return next((shutil.which(n) for n in NAVEGADORES_PATH if shutil.which(n)), None)


def a_docx(md: Path) -> Path:
    out = md.with_suffix(".docx")
    pypandoc.convert_file(str(md), "docx", outputfile=str(out),
                          extra_args=[f"--resource-path={md.parent}"])  # figuras relativas a docs/
    return out


def a_pdf(md: Path) -> Path:
    out = md.with_suffix(".pdf")
    if shutil.which("xelatex"):
        pypandoc.convert_file(str(md), "pdf", outputfile=str(out),
                              extra_args=["--pdf-engine=xelatex", f"--resource-path={md.parent}"])
        return out
    edge = buscar_navegador()
    if edge is None:
        raise RuntimeError("Para el PDF se necesita xelatex (LaTeX) o un navegador Edge, Chrome o Chromium. "
                           "Instala uno de ellos (ver README, sección Instalación). El .docx sí se generó.")
    with tempfile.TemporaryDirectory() as tmp:
        css = Path(tmp) / "estilo.css"
        css.write_text(CSS, encoding="utf-8")
        html = Path(tmp) / (md.stem + ".html")
        pypandoc.convert_file(str(md), "html5", outputfile=str(html),
                              extra_args=["--standalone", "--embed-resources", f"--css={css}",
                                          f"--resource-path={md.parent}"])
        out.unlink(missing_ok=True)
        subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={Path(tmp) / 'perfil_edge'}",  # no se adjunta a un Edge abierto
                        f"--print-to-pdf={out}", html.as_uri()], check=True, capture_output=True)
        # Edge escribe el PDF de forma asíncrona: esperar hasta que exista y deje de crecer
        tam = -1
        for _ in range(60):
            time.sleep(0.5)
            if out.exists() and out.stat().st_size == tam > 0:
                break
            tam = out.stat().st_size if out.exists() else -1
        else:
            raise RuntimeError("Edge no generó el PDF a tiempo.")
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        md = Path(arg).resolve()
        print("->", a_docx(md).name, "|", a_pdf(md).name)
