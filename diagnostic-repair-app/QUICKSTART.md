# Quick Start Guide

Get up and running with the Diagnostic & Repair App in minutes!

## 🚀 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Node.js v16+ installed
- [ ] Flutter SDK v3+ installed
- [ ] ADB (Android Debug Bridge) installed
- [ ] libimobiledevice installed (for iOS support)
- [ ] Git installed
- [ ] A code editor (VS Code recommended)

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd diagnostic-repair-app
```

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env with your settings (optional for local dev)
```

### Step 3: Setup Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Get Flutter dependencies
flutter pub get

# Check Flutter setup
flutter doctor
```

### Step 4: Install Device Tools

#### For Android Support:

**macOS:**
```bash
brew install android-platform-tools
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install android-tools-adb android-tools-fastboot
```

**Windows:**
Download from: https://developer.android.com/studio/releases/platform-tools

#### For iOS Support (macOS/Linux only):

**macOS:**
```bash
brew install libimobiledevice ideviceinstaller
```

**Linux:**
```bash
sudo apt-get install libimobiledevice-tools libimobiledevice-utils
```

## 🎯 Running the Application

### Start Backend Server

```bash
cd backend
npm start
```

You should see:
```
Server running on port 3000
Socket.IO enabled for real-time updates
```

### Start Frontend App

Open a new terminal:

```bash
cd frontend

# For web
flutter run -d chrome

# For Android
flutter run -d android

# For iOS (macOS only)
flutter run -d ios
```

### Test Device Connection

#### Android:

1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device via USB
4. Accept the USB debugging prompt on device

Verify connection:
```bash
adb devices
```

#### iOS:

1. Trust the computer on your iOS device
2. Connect device via USB

Verify connection:
```bash
idevice_id -l
```

## 🧪 Quick Test

### Test Backend API

Open your browser or use curl:

```bash
# Health check
curl http://localhost:3000/health

# List Android devices
curl http://localhost:3000/api/android/devices

# List iOS devices
curl http://localhost:3000/api/ios/devices
```

### Test Frontend

1. Open the app (web at http://localhost:PORT or mobile)
2. You should see the home screen with menu options
3. Navigate to "Diagnostics"
4. Connect a device and run diagnostics

### Create a Test Ticket

1. Click on "Repair Tickets"
2. Click the "+" button
3. Fill in the form:
   - Customer Name: Test Customer
   - Email: test@example.com
   - Phone: +1234567890
   - Device Type: Android
   - Manufacturer: Samsung
   - Model: Galaxy S21
   - Issue: Test issue
4. Click "Create"
5. You should see the ticket in the list

## 📱 Running Diagnostic Scripts

### Android Diagnostics

```bash
cd scripts
node android-diagnostics.js
```

### iOS Diagnostics

```bash
cd scripts
node ios-diagnostics.js
```

### Firmware Flashing (Interactive Mode)

**Android:**
```bash
cd scripts
./android-flash.sh
```

**iOS:**
```bash
cd scripts
./ios-restore.sh
```

## 🔧 Common Setup Issues

### Issue: "adb: command not found"

**Solution:**
- Install Android platform-tools (see prerequisites)
- Add to PATH:
  ```bash
  export PATH=$PATH:~/Library/Android/sdk/platform-tools  # macOS
  export PATH=$PATH:/path/to/android-sdk/platform-tools   # Linux
  ```

### Issue: "idevice_id: command not found"

**Solution:**
- Install libimobiledevice (see prerequisites)
- Verify installation:
  ```bash
  which idevice_id
  ```

### Issue: Flutter doctor shows issues

**Solution:**
Run and follow the recommendations:
```bash
flutter doctor -v
```

### Issue: Backend won't start

**Solution:**
1. Check if port 3000 is already in use:
   ```bash
   lsof -i :3000  # macOS/Linux
   netstat -ano | findstr :3000  # Windows
   ```
2. Change PORT in .env file
3. Kill conflicting process or use different port

### Issue: Android device not detected

**Solution:**
1. Enable USB debugging on device
2. Check USB cable (must support data transfer)
3. Try different USB port
4. Revoke USB debugging authorizations on device and reconnect
5. Run: `adb kill-server && adb start-server`

### Issue: iOS device not detected

**Solution:**
1. Trust the computer on iOS device
2. Check USB cable (must be Apple certified)
3. Restart iOS device
4. Reinstall libimobiledevice:
   ```bash
   brew reinstall libimobiledevice
   ```

## 🎓 Next Steps

### Learn the API

Check out the [API Documentation](API.md) to understand all available endpoints.

### Deploy Your App

Follow the [Deployment Guide](DEPLOYMENT.md) to deploy to production.

### Explore Scripts

Try the automation scripts in the `scripts` directory:
- `android-diagnostics.js` - Run Android diagnostics
- `ios-diagnostics.js` - Run iOS diagnostics
- `android-flash.sh` - Flash Android firmware
- `ios-restore.sh` - Restore iOS firmware

### Customize

1. Update branding in Flutter app
2. Add your logo and colors
3. Customize ticket fields
4. Add custom diagnostic checks

## 📚 Documentation

- [README.md](README.md) - Project overview and setup
- [API.md](API.md) - Complete API reference
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

## 💡 Tips

### Development Tips

1. **Use nodemon for auto-reload**:
   ```bash
   cd backend
   npm run dev
   ```

2. **Hot reload in Flutter**:
   - Press `r` to hot reload
   - Press `R` to hot restart

3. **Check logs**:
   ```bash
   # Backend logs
   tail -f backend/logs/app.log

   # Flutter logs
   flutter logs
   ```

### Testing Tips

1. **Test with multiple devices**:
   - Connect multiple devices
   - Run diagnostics simultaneously
   - Monitor Socket.IO events

2. **Use browser DevTools**:
   - Open Chrome DevTools
   - Monitor Network tab for API calls
   - Check WebSocket connections

3. **Debug ADB issues**:
   ```bash
   adb logcat  # View device logs
   adb shell   # Access device shell
   ```

## 🆘 Getting Help

### If you encounter issues:

1. Check the [Troubleshooting Guide](#common-setup-issues)
2. Review the documentation
3. Check GitHub issues
4. Contact the development team

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend server is running (http://localhost:3000/health)
- [ ] Frontend app is running
- [ ] Android device is detected (if testing Android)
- [ ] iOS device is detected (if testing iOS)
- [ ] Can create a test ticket
- [ ] Can run diagnostics
- [ ] Real-time updates work (Socket.IO)

---

**Congratulations! You're ready to use the Diagnostic & Repair App!** 🎉

For detailed documentation, see [README.md](README.md)
