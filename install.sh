#!/usr/bin/env bash
set -e

echo -e "\033[1;36m================================================================\033[0m"
echo -e "\033[1;36m         AURA-AGI One-Click Installer (Linux / macOS)           \033[0m"
echo -e "\033[1;36m================================================================\033[0m"
echo ""

# 1. Check Python version
echo -e "\033[1;33m[1/5] Checking Python installation...\033[0m"
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo -e "\033[1;31mError: Python 3 is not installed or not in PATH.\033[0m"
    exit 1
fi

if ! $PY_CMD -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    PY_VERSION=$($PY_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "unknown")
    echo -e "\033[1;31mError: AURA-AGI requires Python 3.10 or higher. Found Python $PY_VERSION.\033[0m"
    exit 1
fi
PY_VERSION=$($PY_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "\033[1;32mFound Python $PY_VERSION.\033[0m"

# 2. Create virtual environment
echo -e "\n\033[1;33m[2/5] Creating virtual environment (.venv)...\033[0m"
if [ ! -d ".venv" ]; then
    $PY_CMD -m venv .venv
    echo -e "\033[1;32mVirtual environment created.\033[0m"
else
    echo -e "\033[1;32mVirtual environment already exists.\033[0m"
fi

# 3. Install requirements
echo -e "\n\033[1;33m[3/5] Installing dependencies (this may take a few minutes)...\033[0m"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "\033[1;32mDependencies installed successfully.\033[0m"

# 4. Setup .env files
echo -e "\n\033[1;33m[4/5] Setting up configuration files...\033[0m"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "\033[1;36mCreated .env from .env.example. Please open .env and add your API keys!\033[0m"
    else
        echo -e "\033[1;31mCould not find .env.example. Please create a .env file manually.\033[0m"
    fi
else
    echo -e "\033[1;32m.env already exists.\033[0m"
fi

if [ ! -f "agent_server/.env.agent" ]; then
    if [ -f ".env.agent.example" ]; then
        cp .env.agent.example agent_server/.env.agent
        echo -e "\033[1;32mCreated agent_server/.env.agent from template.\033[0m"
    fi
fi

# 5. Final instructions
echo -e "\n\033[1;32m[5/5] Setup Complete!\033[0m"
echo -e "\033[1;36m================================================================\033[0m"
echo "To start AURA-AGI, run the following commands:"
echo "  1. source .venv/bin/activate"
echo "  2. python main.py"
echo ""
echo -e "\033[1;33mImportant: Don't forget to add your API keys to the .env file!\033[0m"
echo -e "\033[1;36m================================================================\033[0m"
