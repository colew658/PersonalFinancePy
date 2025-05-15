python_version="3.12"

usage() {
    echo: "Usage: $0 [OPTIONS]"
    echo: "Options:"
    echo: "  -h, --help: Display this help message"
    echo: "  -v, --python-version: Python version to use"
}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}


log "Cleaning up previous build"
if [[ "$VIRTUAL_ENV" ]]; then
    log "Deactivating virtual environment"
    deactivate > /dev/null
fi

jupyter kernelspec uninstall venv -y
rm -rf venv
log "Previous build cleaned up"

log "Setting up new build"
log "Creating virtual environment"
python3 -m pip install virtualenv > /dev/null

log "Configuring virtual environment"
python3 -m virtualenv venv --python=python${python_version} > /dev/null
source venv/bin/activate
log "Virtual environment configured"

log "Installing dependencies"
pip install -e .

log "Reactivating virtual environment w/ dependencies installed"
deactivate && source venv/bin/activate

log "Installing pre-commit hooks"
pre-commit install
pre-commit clean

log "Adding virtual environment to Jupyter"
python -m ipykernel install --user --name=venv
