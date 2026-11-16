"""Revisión previa a un push: qué se subiría a GitHub y si hay datos personales.

Uso (desde la raíz del repositorio):
    python scripts/revisar_antes_de_subir.py              # revisa lo pendiente de subir
    python scripts/revisar_antes_de_subir.py --historial  # además, revisa todos los commits

Muestra:
  1. Commits pendientes de subir y archivos que cambian en ellos.
  2. Cambios sin commit: en staging, modificados y archivos nuevos que `git add -A` agregaría.
  3. Archivos sensibles presentes en disco que .gitignore está protegiendo (no se suben).
  4. Alertas: datos o secretos rastreados, números de 9-10 dígitos o correos dentro de los
     archivos, archivos grandes y metadatos de commits (correo de autor numérico, coautores).

Sale con código 1 si encuentra algo que bloquearía la publicación.
Solo usa la biblioteca estándar de Python y git.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Patrones de archivos que nunca deben subirse
SENSIBLES = [
    (re.compile(r"^data/(raw|processed|excluded)/(?!\.gitkeep$)"), "datos del proyecto"),
    (re.compile(r"(^|/)\.streamlit/secrets\.toml$"), "secretos de Streamlit"),
    (re.compile(r"(^|/)\.clave_seudonimo$"), "clave del seudónimo"),
    (re.compile(r"(^|/)\.env$"), "variables de entorno"),
    (re.compile(r"\.xlsx$"), "hoja de cálculo (posibles respuestas originales)"),
]
# Números de cuenta (9-10 dígitos aislados, sin formar parte de base64) y correos
NUMERO = re.compile(rb"(?<![0-9A-Za-z+/=.])[0-9]{9,10}(?![0-9A-Za-z+/=])")
CORREO = re.compile(rb"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
CORREOS_PERMITIDOS = {b"cuenta@pcpuma.acatlan.unam.mx", b"noreply@anthropic.com"}
LIMITE_MB = 50  # GitHub advierte desde 50 MB y rechaza archivos de más de 100 MB


def git(*args: str) -> str:
    # core.quotepath=false: rutas con acentos legibles en lugar de escapadas en octal
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], capture_output=True, text=True,
                       encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def lineas(texto: str) -> list[str]:
    return [l for l in texto.splitlines() if l.strip()]


def contenido(ruta: Path) -> bytes:
    """Bytes a revisar; para .docx/.xlsx se extrae el XML interno (el texto real)."""
    datos = ruta.read_bytes()
    if ruta.suffix in (".docx", ".xlsx"):
        try:
            z = zipfile.ZipFile(ruta)
            datos = b"".join(z.read(n) for n in z.namelist() if n.endswith(".xml"))
        except zipfile.BadZipFile:
            pass
    return datos


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--historial", action="store_true", help="revisa los metadatos de todos los commits")
    args = ap.parse_args()

    rama = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    remoto = f"origin/{rama}"
    tiene_remoto = bool(lineas(git("branch", "-r", "--list", remoto)))
    bloqueos, avisos = [], []

    print(f"Rama: {rama}  ·  remoto: {remoto if tiene_remoto else '(sin rama remota)'}\n")

    # 1. Commits pendientes de subir
    rango = f"{remoto}..HEAD" if tiene_remoto else "HEAD"
    pendientes = lineas(git("log", "--format=%h %s", rango))
    print(f"1. Commits pendientes de subir: {len(pendientes)}")
    for c in pendientes:
        print(f"   {c}")
    archivos_commits = set(lineas(git("diff", "--name-only", rango))) if tiene_remoto else set(lineas(git("ls-files")))
    if pendientes and tiene_remoto:
        print(f"   Archivos que cambian en esos commits ({len(archivos_commits)}):")
        for f in sorted(archivos_commits):
            print(f"     - {f}")

    # 2. Cambios aún sin commit
    staged = set(lineas(git("diff", "--cached", "--name-only")))
    modificados = set(lineas(git("diff", "--name-only")))
    nuevos = set(lineas(git("ls-files", "--others", "--exclude-standard")))
    print(f"\n2. Cambios sin commit: {len(staged)} en staging · {len(modificados)} modificados · "
          f"{len(nuevos)} nuevos que `git add -A` agregaría")
    for titulo, grupo in (("staging", staged), ("modificados", modificados), ("nuevos", nuevos)):
        for f in sorted(grupo):
            print(f"   [{titulo}] {f}")

    # 3. Lo que .gitignore protege (presente en disco, no se sube)
    ignorados = [l[3:] for l in lineas(git("status", "--ignored", "--porcelain")) if l.startswith("!! ")]
    print(f"\n3. Protegido por .gitignore (no se sube): {len(ignorados)} rutas")
    for f in ignorados:
        print(f"   {f}")

    # 4. Alertas
    candidatos = archivos_commits | staged | modificados | nuevos | set(lineas(git("ls-files")))
    for f in sorted(candidatos):
        for patron, motivo in SENSIBLES:
            if patron.search(f) and (f in staged or f in nuevos or f in set(lineas(git("ls-files")))):
                bloqueos.append(f"Archivo sensible que se subiría: {f} ({motivo})")
        ruta = Path(f)
        if not ruta.is_file():
            continue
        if ruta.stat().st_size > LIMITE_MB * 1024 * 1024:
            avisos.append(f"Archivo grande ({ruta.stat().st_size / 1e6:.0f} MB): {f}")
        if ruta.suffix in (".png", ".jpg", ".pdf", ".ico"):
            continue  # binarios sin texto legible
        datos = contenido(ruta)
        nums = set(NUMERO.findall(datos))
        mails = set(CORREO.findall(datos)) - CORREOS_PERMITIDOS
        if nums:
            bloqueos.append(f"Posible número de cuenta en {f}: {len(nums)} coincidencia(s), "
                            f"p. ej. {next(iter(nums))[:2].decode()}*******")
        if mails:
            bloqueos.append(f"Correo en {f}: {', '.join(sorted(m.decode()[:3] + '***' for m in mails))}")

    # Metadatos de commits (lo que GitHub muestra públicamente)
    rango_meta = "HEAD" if args.historial or not tiene_remoto else rango
    autores = lineas(git("log", "--format=%ae|%ce", rango_meta))
    numericos = {e for linea in autores for e in linea.split("|") if e.split("@")[0].isdigit()}
    coautores = sum(1 for l in git("log", "--format=%B", rango_meta).splitlines()
                    if l.lower().startswith("co-authored-by:"))
    alcance = "todo el historial" if rango_meta == "HEAD" else "commits pendientes"
    if numericos:
        avisos.append(f"Correo de autor con parte local numérica (¿número de cuenta?) en {alcance}: "
                      f"{', '.join(e[:2] + '*******@' + e.split('@')[1] for e in numericos)}. "
                      "Ver scripts/reescribir_historial.sh")
    if coautores:
        avisos.append(f"Líneas Co-Authored-By en {alcance}: {coautores}. Ver scripts/reescribir_historial.sh")

    print("\n4. Alertas")
    for b in bloqueos:
        print(f"   ✗ BLOQUEA: {b}")
    for a in avisos:
        print(f"   ! AVISO:   {a}")
    if not bloqueos and not avisos:
        print("   ✓ Sin alertas.")
    print("\nResultado:", "NO subir hasta resolver los bloqueos." if bloqueos else "Se puede subir.")
    return 1 if bloqueos else 0


if __name__ == "__main__":
    sys.exit(main())
