Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "         AURA-AGI One-Click Installer (Windows)                 " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pyVersionStr = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    $pyMajor, $pyMinor = $pyVersionStr.Split('.')
    if ([int]$pyMajor -lt 3 -or ([int]$pyMajor -eq 3 -and [int]$pyMinor -lt 10)) {
        Write-Host "Error: AURA-AGI requires Python 3.10 or higher. Found Python $pyVersionStr." -ForegroundColor Red
        exit 1
    }
    Write-Host "Found Python $pyVersionStr." -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n[2/5] Creating virtual environment (.venv)..." -ForegroundColor Yellow
if (-Not (Test-Path -Path ".venv")) {
    python -m venv .venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}

# Activate virtual environment and install requirements
Write-Host "`n[3/5] Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies." -ForegroundColor Red
    exit 1
}
Write-Host "Dependencies installed successfully." -ForegroundColor Green

# Setup environment variables
Write-Host "`n[4/5] Setting up configuration files..." -ForegroundColor Yellow
if (-Not (Test-Path -Path ".env")) {
    if (Test-Path -Path ".env.example") {
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host "Created .env from .env.example. Please open .env and add your API keys!" -ForegroundColor Cyan
    } else {
        Write-Host "Could not find .env.example. Please create a .env file manually." -ForegroundColor Red
    }
} else {
    Write-Host ".env already exists." -ForegroundColor Green
}

if (-Not (Test-Path -Path "agent_server\.env.agent")) {
    if (Test-Path -Path ".env.agent.example") {
        Copy-Item -Path ".env.agent.example" -Destination "agent_server\.env.agent"
        Write-Host "Created agent_server\.env.agent from template." -ForegroundColor Green
    }
}

# Final instructions
Write-Host "`n[5/5] Setup Complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "To start AURA-AGI, run the following commands:"
Write-Host "  1. .\.venv\Scripts\Activate.ps1"
Write-Host "  2. python main.py"
Write-Host ""
Write-Host "Important: Don't forget to add your API keys to the .env file!" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
