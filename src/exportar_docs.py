"""Exporta documentos Markdown de docs/ a .docx y .pdf.

Uso (desde la raíz del proyecto):
    python src/exportar_docs.py docs/momento_A.md [docs/otro.md ...]

- .docx: pandoc (incluido en el paquete `pypandoc_binary`, no requiere instalación).
- .pdf : si hay xelatex en el PATH se usa `--pdf-engine=xelatex`; si no, se genera
         HTML con estilo y se imprime a PDF con Microsoft Edge en modo headless.
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
header#title-block-header { text-align: center; margin-bottom: 1.5em; }
h1.title { font-size: 18pt; margin-bottom: .2em; }
p.subtitle { font-style: italic; color: #444; margin-top: 0; }
h2 { font-size: 13.5pt; border-bottom: 1px solid #999; padding-bottom: 2px; margin-top: 1.4em; }
h3 { font-size: 11.5pt; margin-top: 1.1em; }
p { text-align: justify; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: .8em 0; page-break-inside: auto; }
th, td { border: 1px solid #bbb; padding: 3px 5px; vertical-align: top; text-align: left; }
th { background: #e9eef4; }
tr { page-break-inside: avoid; }
code { font-family: Consolas, monospace; font-size: 9pt; }
"""

EDGE = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def a_docx(md: Path) -> Path:
    out = md.with_suffix(".docx")
    pypandoc.convert_file(str(md), "docx", outputfile=str(out))
    return out


def a_pdf(md: Path) -> Path:
    out = md.with_suffix(".pdf")
    if shutil.which("xelatex"):
        pypandoc.convert_file(str(md), "pdf", outputfile=str(out), extra_args=["--pdf-engine=xelatex"])
        return out
    edge = next((p for p in EDGE if Path(p).exists()), None)
    if edge is None:
        raise RuntimeError("No hay xelatex ni Microsoft Edge para generar el PDF.")
    with tempfile.TemporaryDirectory() as tmp:
        css = Path(tmp) / "estilo.css"
        css.write_text(CSS, encoding="utf-8")
        html = Path(tmp) / (md.stem + ".html")
        pypandoc.convert_file(str(md), "html5", outputfile=str(html),
                              extra_args=["--standalone", "--embed-resources", f"--css={css}"])
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
