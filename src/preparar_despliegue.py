"""Genera el secreto con los datos mínimos del tablero para Streamlit Community Cloud.

Uso (desde la raíz, después de ejecutar los cuadernos 01 a 03):
    python src/preparar_despliegue.py

Escribe .streamlit/secrets.toml (excluido de Git). Su contenido se pega en
Streamlit Community Cloud → la app → Settings → Secrets. Los datos nunca se suben al repositorio.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tablero as tb  # noqa: E402
from datos import RAIZ  # noqa: E402

base = tb.cargar_base()
publicable = tb.base_publicable(base)
csv = publicable.to_csv(index=False, lineterminator="\n")

# Salvaguardas: sin secuencias de 9-10 dígitos (cuentas), sin correos, sin triple comilla (rompe el TOML)
assert not re.search(r"(?<![0-9.])[0-9]{9,10}(?![0-9])", csv), "posible número de cuenta en el CSV"
assert not re.search(r"[\w.+-]+@[\w-]+\.\w+", csv), "posible correo en el CSV"
assert "'''" not in csv

destino = RAIZ / ".streamlit" / "secrets.toml"
destino.parent.mkdir(exist_ok=True)
destino.write_text("[datos]\ntablero_csv = '''\n" + csv + "'''\n", encoding="utf-8")

print(f"Escrito {destino.relative_to(RAIZ)}: {len(publicable)} estudiantes × {publicable.shape[1]} columnas, "
      f"{destino.stat().st_size / 1024:.1f} KB")
print("Copia TODO su contenido en Streamlit Community Cloud → Settings → Secrets. No lo subas a Git.")
