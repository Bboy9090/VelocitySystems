#!/bin/bash

echo "========================================"
echo "  Bobby Dev Panel - Desktop App"
echo "  Pandora Codex"
echo "========================================"
echo ""

# Get script directory
cd "$(dirname "$0")"

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

if ! command -v cargo &> /dev/null; then
    echo "ERROR: Rust not found!"
    echo "Please install Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

echo ""
echo "Installing dependencies (if needed)..."
npm install

echo ""
echo "Starting desktop app..."
echo ""
npm run tauri dev
