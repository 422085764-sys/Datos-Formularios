#!/usr/bin/env bash
# Reescribe el historial de Git para:
#   1. Quitar las líneas "Co-Authored-By: Claude ..." de todos los mensajes de commit.
#   2. (Opcional) Cambiar el correo de autor/committer, p. ej. por tu correo noreply de GitHub,
#      para no publicar el correo institucional (cuya parte local es el número de cuenta).
#
# Uso (desde la raíz del repositorio, en Git Bash):
#   bash scripts/reescribir_historial.sh --simular
#   bash scripts/reescribir_historial.sh
#   bash scripts/reescribir_historial.sh --email 12345678+usuario@users.noreply.github.com
#
# Qué hace:
#   - Exige un árbol de trabajo limpio (sin cambios sin commit).
#   - Crea una rama de respaldo "respaldo-antes-de-reescribir" con el historial original.
#   - Reescribe todos los commits de la rama actual con git filter-branch.
#   - Si se pasa --email, configura ese correo SOLO para este repositorio (commits futuros).
#   - NO sube nada: al final indica el comando de push forzado para que lo ejecutes tú.
#
# Deshacer (antes de hacer push): git reset --hard respaldo-antes-de-reescribir
set -euo pipefail

SIMULAR=0
NUEVO_EMAIL=""
NUEVO_NOMBRE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --simular) SIMULAR=1 ;;
    --email) NUEVO_EMAIL="${2:?falta el correo después de --email}"; shift ;;
    --nombre) NUEVO_NOMBRE="${2:?falta el nombre después de --nombre}"; shift ;;
    -h|--help) sed -n '2,21p' "$0"; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; exit 2 ;;
  esac
  shift
done

cd "$(git rev-parse --show-toplevel)"
RAMA="$(git rev-parse --abbrev-ref HEAD)"
VIEJO_EMAIL="$(git config user.email || true)"
TOTAL="$(git rev-list --count HEAD)"
CON_COAUTOR="$(git log --format=%B HEAD | grep -ci '^Co-Authored-By: Claude' || true)"
CON_EMAIL="$(git log --format='%ae%n%ce' HEAD | grep -cxF "$VIEJO_EMAIL" || true)"

echo "Rama: $RAMA · commits: $TOTAL"
echo "Líneas Co-Authored-By de Claude: $CON_COAUTOR"
if [ -n "$NUEVO_EMAIL" ]; then
  echo "Correo actual -> nuevo: ${VIEJO_EMAIL:0:2}*******@${VIEJO_EMAIL#*@} -> $NUEVO_EMAIL ($CON_EMAIL apariciones como autor/committer)"
fi

if [ "$SIMULAR" = 1 ]; then
  echo "Modo simulación: no se modificó nada."
  exit 0
fi

if [ -n "$(git status --porcelain)" ]; then
  echo "Hay cambios sin commit. Haz commit o guárdalos (git stash) antes de reescribir." >&2
  exit 1
fi

git branch -f respaldo-antes-de-reescribir HEAD
echo "Respaldo creado: rama respaldo-antes-de-reescribir"

export VIEJO_EMAIL NUEVO_EMAIL NUEVO_NOMBRE
export FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch -f \
  --msg-filter 'grep -vi "^Co-Authored-By: Claude" | git stripspace' \
  --env-filter '
    if [ -n "$NUEVO_EMAIL" ]; then
      if [ "$GIT_AUTHOR_EMAIL" = "$VIEJO_EMAIL" ]; then
        export GIT_AUTHOR_EMAIL="$NUEVO_EMAIL"
        if [ -n "$NUEVO_NOMBRE" ]; then export GIT_AUTHOR_NAME="$NUEVO_NOMBRE"; fi
      fi
      if [ "$GIT_COMMITTER_EMAIL" = "$VIEJO_EMAIL" ]; then
        export GIT_COMMITTER_EMAIL="$NUEVO_EMAIL"
        if [ -n "$NUEVO_NOMBRE" ]; then export GIT_COMMITTER_NAME="$NUEVO_NOMBRE"; fi
      fi
    fi
    true' \
  -- "$RAMA"

# Limpia la referencia de respaldo interna de filter-branch (el respaldo propio se conserva)
git update-ref -d "refs/original/refs/heads/$RAMA" 2>/dev/null || true

if [ -n "$NUEVO_EMAIL" ]; then
  git config user.email "$NUEVO_EMAIL"
  if [ -n "$NUEVO_NOMBRE" ]; then git config user.name "$NUEVO_NOMBRE"; fi
  echo "Correo configurado para este repositorio: $NUEVO_EMAIL"
fi

echo
echo "Verificación:"
echo "  Líneas Co-Authored-By restantes: $(git log --format=%B HEAD | grep -ci '^Co-Authored-By' || true)"
echo "  Correos de autor en el historial:"
git log --format='%ae' HEAD | sort | uniq -c | sed -E 's/ ([0-9]{2})[0-9]{7,}@/ \1*******@/'
echo
echo "Si todo está bien, sube el historial nuevo (reemplaza el de GitHub):"
echo "  git push --force-with-lease origin $RAMA"
echo "Para deshacer antes del push: git reset --hard respaldo-antes-de-reescribir"
