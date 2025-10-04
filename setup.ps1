$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install pre-commit

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

pre-commit install

Write-Host "Setup complete" -ForegroundColor Green
