$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (!(Test-Path .venv)) {
  python -m venv .venv
}

# Activate venv
. .\.venv\Scripts\Activate.ps1

# Make sure deps exist (quiet if already present)
pip install -q fastapi uvicorn

# Run
python -m src.main
