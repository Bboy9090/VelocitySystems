# Desktop App Build Instructions

## Quick Start

### 1. Install Prerequisites

**Rust**:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**Node.js** (v18+):
```bash
# macOS
brew install node

# Linux
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**System Dependencies**:

macOS:
```bash
brew install android-platform-tools libimobiledevice
```

Linux:
```bash
sudo apt-get install android-tools-adb libimobiledevice6 \
  libwebkit2gtk-4.0-dev build-essential curl wget file \
  libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev
```

Windows:
- Install [Rust](https://rustup.rs/)
- Install [Node.js](https://nodejs.org/)
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Download ADB and libimobiledevice-win32

### 2. Setup Project

```bash
cd desktop
npm install
```

### 3. Development

```bash
npm run tauri dev
```

### 4. Production Build

```bash
npm run tauri build
```

## Project Structure

```
desktop/
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── styles/            # CSS
│   └── App.tsx            # Main app
├── src-tauri/             # Rust backend
│   └── src/
│       ├── main.rs        # Entry point
│       ├── commands.rs   # Tauri commands
│       └── python.rs    # Python integration
└── package.json          # Dependencies
```

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: Rust + Tauri
- **Integration**: Python modules via subprocess
- **UI**: Dark cyber-forensics theme

## Troubleshooting

### Python Module Not Found
- Ensure `bobby_dev_panel` is in parent directory or same directory
- Check Python path detection in `python.rs`

### Build Errors
- Update Rust: `rustup update`
- Reinstall dependencies: `npm install`
- Clear cache: `rm -rf node_modules target`
