"""Inserta tablas generadas desde el código en los documentos Markdown.

Reemplaza el contenido entre `<!-- anexo:NOMBRE -->` y `<!-- /anexo -->`, de modo que
los anexos siempre coinciden con la fuente (p. ej. el diccionario de variables).

Uso: python src/anexos.py
"""
import re
from pathlib import Path

import pandas as pd

from datos import DOCS_DIR
from diccionario import DICCIONARIO


def actualizar_anexo(md: Path, nombre: str, tabla: pd.DataFrame) -> None:
    texto = md.read_text(encoding="utf-8")
    patron = re.compile(rf"(<!-- anexo:{nombre} -->\n).*?(<!-- /anexo -->)", re.S)
    if not patron.search(texto):
        raise ValueError(f"No se encontró el marcador anexo:{nombre} en {md.name}")
    contenido = tabla.to_markdown(index=False) + "\n"
    md.write_text(patron.sub(lambda m: m.group(1) + contenido + m.group(2), texto), encoding="utf-8")


if __name__ == "__main__":
    dic = DICCIONARIO.rename(columns={
        "doc": "Doc", "pregunta_n": "P", "variable": "Variable", "pregunta": "Pregunta",
        "respuesta": "Respuesta", "codificacion": "Codificación prevista", "uso": "Uso",
    })
    actualizar_anexo(DOCS_DIR / "tecnico.md", "diccionario", dic)
    print("Anexo A actualizado en docs/tecnico.md")
