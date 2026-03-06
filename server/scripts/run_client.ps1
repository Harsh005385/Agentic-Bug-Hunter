$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverRoot = Split-Path -Parent $root

Set-Location $serverRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  Write-Host "Virtualenv not found. Run scripts\run_server.ps1 once first."
  exit 1
}

.\.venv\Scripts\python.exe .\client_test.py

