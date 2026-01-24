# 🚀 START HERE - How to Run the Desktop App

## 📍 Location

The desktop app is located at:
```
bobby_dev_panel/desktop/
```

## ⚡ Quick Start

### Step 1: Open Terminal/Command Prompt

**Windows**:
- Press `Win + R`, type `cmd`, press Enter
- Or press `Win + X`, select "Terminal"

**macOS**:
- Press `Cmd + Space`, type "Terminal", press Enter

**Linux**:
- Press `Ctrl + Alt + T`

### Step 2: Navigate to Desktop Folder

```bash
cd "C:\Users\Bobby\Documents\Velocity_Systems_FULL_Masterclass_Repo\bobby_dev_panel\desktop"
```

Or if you're already in the repo:
```bash
cd bobby_dev_panel/desktop
```

### Step 3: Install Dependencies (First Time Only)

```bash
npm install
```

This will take 2-5 minutes the first time.

### Step 4: Run the App

```bash
npm run tauri dev
```

The app window will open automatically!

## 📦 Building for Production (Optional)

To create an installable app:

```bash
npm run tauri build
```

**Output locations**:
- **Windows**: `src-tauri/target/release/bundle/msi/Bobby Dev Panel_1.0.0_x64_en-US.msi`
- **macOS**: `src-tauri/target/release/bundle/macos/Bobby Dev Panel.app`
- **Linux**: `src-tauri/target/release/bundle/appimage/Bobby Dev Panel.AppImage`

## 🎯 What You'll See

1. **App Window Opens** (1400x900)
2. **Sidebar** on the left with navigation
3. **Status Bar** at the top showing connection status
4. **Main Area** with dashboard or device list

## ⚠️ Prerequisites Check

Before running, make sure you have:

1. **Node.js** installed:
   ```bash
   node --version
   ```
   Should show v18 or higher

2. **Rust** installed:
   ```bash
   rustc --version
   ```
   If not installed, run: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

3. **Python** installed:
   ```bash
   python3 --version
   ```
   Should show Python 3.8 or higher

4. **ADB** (for Android):
   ```bash
   adb version
   ```

5. **libimobiledevice** (for iOS, optional):
   ```bash
   idevice_id -l
   ```

## 🐛 Troubleshooting

### "npm: command not found"
- Install Node.js from https://nodejs.org/

### "cargo: command not found"
- Install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

### "Python module not found"
- Make sure you're in the `bobby_dev_panel/desktop` folder
- The app looks for `bobby_dev_panel` in the parent directory

### App won't start
- Check console for errors
- Make sure all prerequisites are installed
- Try: `npm install` again

## 📝 Notes

- **First Run**: May take 5-10 minutes (compiling Rust)
- **Subsequent Runs**: Much faster (< 30 seconds)
- **Development Mode**: Auto-reloads on code changes
- **Production Build**: Creates installable package
