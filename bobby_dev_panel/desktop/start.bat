@echo off
echo ========================================
echo   Bobby Dev Panel - Desktop App
echo   Pandora Codex
echo ========================================
echo.

cd /d "%~dp0"

echo Checking prerequisites...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

where cargo >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Rust not found!
    echo Please install Rust from https://rustup.rs/
    pause
    exit /b 1
)

echo.
echo Installing dependencies (if needed)...
call npm install

echo.
echo Starting desktop app...
echo.
call npm run tauri dev

pause
