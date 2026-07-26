#!/usr/bin/env bash
# Development runner (Linux/macOS).
# Usage: ./scripts/run_dev.sh
set -euo pipefail

# Resolve project root regardless of where the script is called from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

VENV_DIR="${VENV_DIR:-venv}"
PYTHON="${PYTHON:-python3}"

# Create the virtualenv on first run.
if [ ! -d "$VENV_DIR" ]; then
    echo ">> Creating virtualenv in $VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.dev}"

echo ">> Installing dependencies"
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

echo ">> Applying migrations"
python manage.py migrate --no-input

echo ">> Starting development server (Daphne ASGI) on http://0.0.0.0:8000"
# Daphne serves both HTTP and WebSocket (Channels).
exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
