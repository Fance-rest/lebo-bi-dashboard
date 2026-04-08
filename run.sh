#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# ── Python backend setup ──
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

# ── Frontend build ──
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    (cd frontend && npm install --silent)
fi

echo "Building frontend..."
(cd frontend && npm run build --silent)

# ── Launch ──
echo ""
echo "  Dashboard running at: http://localhost:8000"
echo ""

PYTHONPATH=. python -m backend.main
