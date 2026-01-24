# Bobby Dev Panel - Desktop Application

Enterprise-grade desktop application built with Tauri (Rust + React/TypeScript).

## Features

- 🖥️ **Native Desktop App**: Fast, secure, cross-platform
- 🎨 **Modern UI**: Dark cyber-forensics aesthetic
- 📊 **Real-time Dashboard**: Live device metrics and health scores
- 📱 **Multi-Device Support**: Android + iOS device management
- 📈 **Interactive Charts**: Health trends and analytics
- 🔒 **Enterprise Security**: Immutable evidence chains

## Prerequisites

### Required Tools

1. **Rust** (for Tauri backend)
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. **Node.js** (v18+) and npm
   ```bash
   # macOS
   brew install node
   
   # Linux
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Python 3.8+** (for Bobby Dev Panel modules)
   ```bash
   # Already installed on most systems
   python3 --version
   ```

4. **Platform Tools**
   - **Android**: ADB (Android Debug Bridge)
   - **iOS**: libimobiledevice

### System Dependencies

**macOS**:
```bash
brew install android-platform-tools libimobiledevice
```

**Linux**:
```bash
sudo apt-get install android-tools-adb libimobiledevice6 libwebkit2gtk-4.0-dev \
  build-essential curl wget file libssl-dev libgtk-3-dev libayatana-appindicator3-dev \
  librsvg2-dev
```

**Windows**:
- Install [Rust](https://rustup.rs/)
- Install [Node.js](https://nodejs.org/)
- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Download ADB from Android SDK Platform Tools
- Download libimobiledevice-win32

## Installation

1. **Install Dependencies**:
   ```bash
   cd desktop
   npm install
   ```

2. **Build Rust Backend**:
   ```bash
   cd src-tauri
   cargo build
   cd ..
   ```

3. **Development Mode**:
   ```bash
   npm run tauri dev
   ```

4. **Production Build**:
   ```bash
   npm run tauri build
   ```

## Project Structure

```
desktop/
├── src/                    # React/TypeScript frontend
│   ├── components/         # UI components
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── DeviceList.tsx # Device selection
│   │   ├── Sidebar.tsx    # Navigation
│   │   └── StatusBar.tsx  # Status indicators
│   ├── styles/            # CSS styles
│   ├── App.tsx            # Main app component
│   └── main.tsx           # Entry point
├── src-tauri/             # Rust backend
│   ├── src/
│   │   ├── main.rs        # Tauri app entry
│   │   ├── commands.rs    # Tauri commands
│   │   └── python.rs     # Python integration
│   └── Cargo.toml        # Rust dependencies
├── package.json          # Node.js dependencies
├── vite.config.ts        # Vite configuration
└── tauri.conf.json       # Tauri configuration
```

## Architecture

### Frontend (React/TypeScript)
- **Framework**: React 18 with TypeScript
- **Styling**: CSS with custom properties (dark theme)
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React
- **Routing**: React Router (for future expansion)

### Backend (Rust/Tauri)
- **Framework**: Tauri 1.5
- **Python Integration**: Calls Python modules via subprocess
- **Commands**: Exposes Python functions as Tauri commands
- **Security**: Sandboxed with proper permissions

### Integration
- Tauri commands call Python modules
- JSON serialization for data exchange
- Real-time updates via polling
- Error handling and user feedback

## UI Features

### Dashboard
- **Health Score**: Large, prominent display
- **Metrics Grid**: Battery, Performance, Security, Sensors
- **Trend Charts**: 30-day health score trends
- **Recommendations**: Actionable device recommendations

### Device List
- **Multi-Device Support**: Shows all connected devices
- **Platform Badges**: Android/iOS indicators
- **Status Indicators**: Connection status
- **Quick Selection**: Click to select device

### Sidebar Navigation
- **Dashboard**: Main overview
- **Devices**: Device management
- **Intake**: Full device intake
- **History**: Historical tracking
- **Monitor**: Real-time monitoring
- **Forensics**: Security analysis
- **AI Analytics**: Predictive analytics
- **Settings**: Configuration

## Building for Production

### macOS
```bash
npm run tauri build
# Output: src-tauri/target/release/bundle/macos/Bobby Dev Panel.app
```

### Linux
```bash
npm run tauri build
# Output: src-tauri/target/release/bundle/appimage/Bobby Dev Panel.AppImage
# or: src-tauri/target/release/bundle/deb/bobby-dev-panel_1.0.0_amd64.deb
```

### Windows
```bash
npm run tauri build
# Output: src-tauri/target/release/bundle/msi/Bobby Dev Panel_1.0.0_x64_en-US.msi
```

## Development

### Hot Reload
```bash
npm run tauri dev
```
- Frontend: Vite dev server (http://localhost:1420)
- Backend: Rust compiled on changes
- Python: Uses installed bobby_dev_panel module

### Debugging
- **Frontend**: Browser DevTools (F12)
- **Backend**: Rust debugger or `println!`
- **Python**: Check console output

## Configuration

### Tauri Config (`tauri.conf.json`)
- Window size: 1400x900 (min: 1200x800)
- App identifier: `com.bobbyworkshop.devpanel`
- Permissions: Shell, FS, Dialog, Notification, HTTP

### Python Path
The app automatically detects `bobby_dev_panel` in:
1. Current directory
2. Parent directory
3. Next to executable (production)
4. Fallback: `bobby_dev_panel` in current dir

## Troubleshooting

### Python Module Not Found
- Ensure `bobby_dev_panel` is in the correct location
- Check Python path in `python.rs`
- Verify Python 3.8+ is installed

### ADB/iOS Tools Not Found
- Install platform tools (see Prerequisites)
- Add to PATH if needed
- Check with `adb version` and `idevice_id -l`

### Build Errors
- **Rust**: Run `rustup update`
- **Node**: Run `npm install` again
- **Tauri**: Check Tauri version compatibility

## Performance

- **Startup**: < 2 seconds
- **Device Detection**: < 1 second
- **Dashboard Load**: < 3 seconds
- **Memory Usage**: ~150-200 MB
- **CPU Usage**: < 5% idle

## Security

- **Sandboxed**: Tauri security model
- **No Network**: All operations local (unless explicitly enabled)
- **File Access**: Limited to app data directories
- **Python Execution**: Controlled subprocess calls

## License

Part of Pandora Codex ecosystem.
