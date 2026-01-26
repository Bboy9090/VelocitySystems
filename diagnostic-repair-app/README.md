# Diagnostic & Repair App

A comprehensive full-stack application for managing device repairs, running diagnostics, and flashing firmware for Android and iOS devices.

## 🚀 Features

### Backend (Node.js & Express)
- **RESTful APIs** for repair ticket management
- **Real-time updates** via Socket.IO
- **Android diagnostics** via ADB (adbkit)
- **iOS diagnostics** via libimobiledevice
- **Firmware flashing** automation
- **Device state management** (Fastboot, Recovery, DFU modes)

### Frontend (Flutter)
- **Cross-platform** (Android & iOS)
- **Responsive UI** with Material Design
- **Real-time diagnostics** dashboard
- **Repair ticket management**
- **QR/Barcode scanning** (coming soon)
- **Live data streaming** from devices

### Scripts
- **Android diagnostics** script
- **iOS diagnostics** script
- **Android firmware flashing** (Fastboot)
- **iOS firmware restore** (libimobiledevice)

## 📋 Prerequisites

### Backend Requirements
- Node.js (v16 or later)
- npm or yarn
- ADB (Android Debug Bridge) - for Android support
- libimobiledevice - for iOS support

### Frontend Requirements
- Flutter SDK (v3.0 or later)
- Dart SDK
- Android Studio (for Android development)
- Xcode (for iOS development on macOS)

### System Requirements

#### For Android Support:
```bash
# macOS
brew install android-platform-tools

# Linux
sudo apt-get install android-tools-adb android-tools-fastboot

# Windows
Download Android SDK Platform-Tools from:
https://developer.android.com/studio/releases/platform-tools
```

#### For iOS Support:
```bash
# macOS
brew install libimobiledevice ideviceinstaller

# Linux
sudo apt-get install libimobiledevice-tools libimobiledevice-utils
```

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd diagnostic-repair-app
```

### 2. Backend Setup

```bash
cd backend
npm install
```

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
PORT=3000
NODE_ENV=development
```

Start the backend server:
```bash
npm start

# Or for development with auto-reload:
npm run dev
```

The server will be running at `http://localhost:3000`

### 3. Frontend Setup

```bash
cd frontend
flutter pub get
```

Update API endpoint in `lib/main.dart`:
```dart
apiService = ApiService(baseUrl: 'http://YOUR_BACKEND_URL/api');
socketService = SocketService(serverUrl: 'http://YOUR_BACKEND_URL');
```

Run the Flutter app:
```bash
# For web
flutter run -d chrome

# For Android
flutter run -d android

# For iOS
flutter run -d ios
```

## 📱 Usage

### Starting the Backend

```bash
cd backend
npm start
```

### Running Diagnostic Scripts

#### Android Diagnostics:
```bash
cd scripts
node android-diagnostics.js [device-id]
```

#### iOS Diagnostics:
```bash
cd scripts
node ios-diagnostics.js [device-udid]
```

#### Android Firmware Flashing:
```bash
cd scripts
chmod +x android-flash.sh
./android-flash.sh [device-id] [firmware-directory]
```

#### iOS Firmware Restore:
```bash
cd scripts
chmod +x ios-restore.sh
./ios-restore.sh [device-udid] [ipsw-path]
```

## 🌐 API Documentation

### Repair Tickets

#### Get All Tickets
```
GET /api/tickets
Query params: status, customerId
```

#### Get Single Ticket
```
GET /api/tickets/:id
```

#### Create Ticket
```
POST /api/tickets
Body: {
  customer: { name, email, phone },
  device: { type, manufacturer, model, serialNumber },
  issue: { description, category, severity }
}
```

#### Update Ticket
```
PUT /api/tickets/:id
Body: { ...updates }
```

#### Update Ticket Status
```
PATCH /api/tickets/:id/status
Body: { status, note }
```

### Android Diagnostics

#### List Android Devices
```
GET /api/android/devices
```

#### Get Device Info
```
GET /api/android/devices/:deviceId/info
```

#### Get Battery Info
```
GET /api/android/devices/:deviceId/battery
```

#### Run Full Diagnostics
```
POST /api/android/devices/:deviceId/diagnostics
```

#### Device State Management
```
POST /api/android/devices/:deviceId/fastboot    # Enter Fastboot mode
POST /api/android/devices/:deviceId/recovery    # Enter Recovery mode
POST /api/android/devices/:deviceId/reboot      # Reboot device
```

### iOS Diagnostics

#### List iOS Devices
```
GET /api/ios/devices
```

#### Get Device Info
```
GET /api/ios/devices/:deviceId/info
```

#### Get Battery Info
```
GET /api/ios/devices/:deviceId/battery
```

#### Run Full Diagnostics
```
POST /api/ios/devices/:deviceId/diagnostics
```

#### Device State Management
```
POST /api/ios/devices/:deviceId/recovery    # Enter Recovery mode
POST /api/ios/devices/:deviceId/dfu         # DFU mode instructions
POST /api/ios/devices/:deviceId/reboot      # Reboot device
```

### Firmware Flashing

#### Flash Android Partition
```
POST /api/firmware/android/flash
Body: { deviceId, firmwarePath, partition }
```

#### Flash Android Full ROM
```
POST /api/firmware/android/flash-all
Body: { deviceId, firmwareDir }
```

#### Restore iOS Firmware
```
POST /api/firmware/ios/restore
Body: { deviceId, ipswPath }
```

## 🔌 Socket.IO Events

### Client → Server
- `subscribe-ticket`: Subscribe to ticket updates

### Server → Client
- `ticket-created`: New ticket created
- `ticket-updated`: Ticket updated
- `ticket-status-changed`: Ticket status changed
- `diagnostics-started`: Diagnostics started
- `diagnostics-completed`: Diagnostics completed
- `battery-update`: Real-time battery update
- `flash-started`: Firmware flash started
- `flash-progress`: Firmware flash progress
- `flash-completed`: Firmware flash completed
- `flash-failed`: Firmware flash failed

## 🚀 Deployment

### Backend Deployment (Heroku)

1. Install Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Login to Heroku:
```bash
heroku login
```

3. Create Heroku app:
```bash
cd backend
heroku create your-app-name
```

4. Set environment variables:
```bash
heroku config:set NODE_ENV=production
```

5. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Backend Deployment (AWS)

1. Use AWS Elastic Beanstalk or EC2
2. Set up Node.js environment
3. Configure security groups to allow necessary ports
4. Deploy using AWS CLI or console

### Frontend Deployment (Firebase Hosting)

1. Install Firebase CLI:
```bash
npm install -g firebase-tools
```

2. Login to Firebase:
```bash
firebase login
```

3. Initialize Firebase:
```bash
cd frontend
firebase init hosting
```

4. Build Flutter web:
```bash
flutter build web
```

5. Deploy:
```bash
firebase deploy
```

## 🔐 Security Considerations

- Always use HTTPS in production
- Implement authentication/authorization
- Validate all inputs
- Secure API endpoints
- Use environment variables for secrets
- Implement rate limiting
- Enable CORS properly
- Keep dependencies updated

## 🧪 Testing

### Backend Tests
```bash
cd backend
npm test
```

### Frontend Tests
```bash
cd frontend
flutter test
```

## 📝 License

All rights reserved.

## 🤝 Contributing

This is a proprietary project. Contributions are restricted to authorized team members only.

## 📞 Support

For issues or questions, contact the development team.

---

**Built with ❤️ by Velocity Systems**
