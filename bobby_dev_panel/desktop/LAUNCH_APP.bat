@echo off
title Bobby Dev Panel - Desktop App
color 0A

echo.
echo ========================================
echo   BOBBY DEV PANEL - DESKTOP APP
echo   Pandora Codex
echo ========================================
echo.
echo Location: %CD%
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/4] Checking Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo    [X] Node.js not found!
    echo.
    echo    Please install Node.js from: https://nodejs.org/
    echo    Then run this script again.
    echo.
    pause
    exit /b 1
)
echo    [✓] Node.js found
node --version

echo.
echo [2/4] Checking Rust...
where cargo >nul 2>&1
if %errorlevel% neq 0 (
    echo    [X] Rust not found!
    echo.
    echo    Please install Rust from: https://rustup.rs/
    echo    Or run: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs ^| sh
    echo    Then run this script again.
    echo.
    pause
    exit /b 1
)
echo    [✓] Rust found
cargo --version

echo.
echo [3/4] Installing dependencies...
if not exist "node_modules" (
    echo    Installing npm packages (this may take a few minutes)...
    call npm install
    if %errorlevel% neq 0 (
        echo    [X] npm install failed!
        pause
        exit /b 1
    )
) else (
    echo    [✓] Dependencies already installed
)

echo.
echo [4/4] Starting desktop app...
echo.
echo    The app window will open shortly...
echo    (First run may take 5-10 minutes to compile Rust)
echo.
echo ========================================
echo.

call npm run tauri dev

if %errorlevel% neq 0 (
    echo.
    echo [X] App failed to start!
    echo.
    echo Troubleshooting:
    echo 1. Make sure Node.js and Rust are installed
    echo 2. Make sure you're in the desktop folder
    echo 3. Try running: npm install
    echo.
    pause
)
