#!/bin/bash

echo "[*] Checking for Python..."

# Install Python if not present
if ! command -v python &> /dev/null; then
    echo "[+] Python not found. Installing..."
    if command -v pkg &> /dev/null; then
        pkg install -y python
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-pip
        alias python=python3
    else
        echo "❌ Unsupported package manager. Install Python manually."
        exit 1
    fi
fi

# Ensure pip exists
if ! command -v pip &> /dev/null; then
    echo "[+] Installing pip..."
    python -m ensurepip --upgrade || curl -sS https://bootstrap.pypa.io/get-pip.py | python
fi

echo "[*] Installing requirements..."
pip install -U -r requirements.txt

echo "[*] Starting ban-tool..."
python backup.py
