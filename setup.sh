#!/usr/bin/env bash

# ========================
# Configuration
# ========================
python_version="3.12"

# ========================
# Functions
# ========================

usage() {
    echo "Usage: source setup.sh [OPTIONS]"
    echo "Options:"
    echo "  -h, --help              Display this help message"
    echo "  -v, --python-version    Specify Python version to use (e.g. 3.11)"
}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Ensure script is sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "⚠️  Please run this script using 'source setup.sh' so the virtual environment is activated in your current shell."
    exit 1
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--python-version)
            python_version="$2"
            shift 2
            ;;
        -h|--help)
            usage
            return 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            return 1
            ;;
    esac
done

# ========================
# Cleanup
# ========================
log "Cleaning up previous build"

if [[ -n "$VIRTUAL_ENV" && "$(type -t deactivate)" == "function" ]]; then
    log "Deactivating existing virtual environment"
    deactivate
fi


if jupyter kernelspec list 2>/dev/null | grep -q "^venv\s"; then
    jupyter kernelspec uninstall venv -y > /dev/null 2>&1
    log "Jupyter kernel 'venv' uninstalled"
fi

rm -rf venv
log "Previous build cleaned up"

# ========================
# Create virtual environment
# ========================
log "Setting up new build"
log "Installing virtualenv if not present"
python -m pip install --quiet virtualenv

log "Finding Python binary for version ${python_version}"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows Git Bash: use py launcher if available
    if command -v py >/dev/null 2>&1; then
        python_cmd="py -${python_version}"
    else
        log "⚠️  'py' launcher not found, falling back to 'python'"
        python_cmd="python"
    fi
else
    # Unix/macOS
    python_cmd=$(command -v "python${python_version}" || command -v python)
fi

# Confirm it works
if ! $python_cmd --version >/dev/null 2>&1; then
    log "❌ ERROR: Cannot run Python with command: $python_cmd"
    return 1
fi

log "Creating virtual environment using: $python_cmd"
$python_cmd -m virtualenv venv --quiet || {
    log "❌ ERROR: Failed to create virtual environment"
    return 1
}


# ========================
# Activate virtual environment
# ========================
if [[ -f "venv/Scripts/activate" ]]; then
    source "venv/Scripts/activate"
elif [[ -f "venv/bin/activate" ]]; then
    source "venv/bin/activate"
else
    log "❌ ERROR: Could not find virtual environment activation script"
    return 1
fi

log "Virtual environment activated"

# ========================
# Install project dependencies
# ========================
log "Installing dependencies"
pip install -e . > /dev/null || {
    log "❌ ERROR: Failed to install dependencies"
    return 1
}

log "Dependencies installed"

# ========================
# Pre-commit hooks
# ========================
log "Installing pre-commit hooks"
pre-commit install
pre-commit clean

# ========================
# Register Jupyter kernel
# ========================
log "Adding virtual environment to Jupyter"
python -m ipykernel install --user --name=venv --display-name "venv" > /dev/null
log "Jupyter kernel registered as 'venv'"

log "✅ Setup complete. You are now in the virtual environment."

