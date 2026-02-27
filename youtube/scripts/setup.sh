#!/bin/bash
# Auto-setup virtual environment and dependencies

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PLUGIN_DIR/.venv"
REQUIREMENTS="$PLUGIN_DIR/requirements.txt"
MARKER="$PLUGIN_DIR/.setup-complete"

# Skip if already set up
[ -f "$MARKER" ] && exit 0

echo "Setting up youtube plugin..." >&2

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    if command -v uv &> /dev/null; then
        uv venv "$VENV_DIR" >&2
    else
        python3 -m venv "$VENV_DIR" >&2
    fi
fi

# Install dependencies
if command -v uv &> /dev/null; then
    cd "$PLUGIN_DIR" && uv pip install -r "$REQUIREMENTS" >&2
else
    "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS" >&2
fi

# Create marker file
touch "$MARKER"
echo "Setup complete!" >&2
