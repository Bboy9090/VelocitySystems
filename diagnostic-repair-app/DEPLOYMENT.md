# Deployment Guide

This guide provides detailed instructions for deploying the Diagnostic & Repair App to various platforms.

## 📋 Table of Contents
1. [Backend Deployment](#backend-deployment)
   - [Heroku](#heroku-deployment)
   - [AWS](#aws-deployment)
   - [DigitalOcean](#digitalocean-deployment)
2. [Frontend Deployment](#frontend-deployment)
   - [Firebase Hosting](#firebase-hosting)
   - [Netlify](#netlify-alternative)
3. [Firebase Cloud Messaging](#firebase-cloud-messaging)
4. [Environment Configuration](#environment-configuration)

---

## Backend Deployment

### Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Step-by-Step Instructions

1. **Install Heroku CLI** (if not already installed):
```bash
# macOS
brew install heroku/brew/heroku

# Windows (using Chocolatey)
choco install heroku-cli

# Linux (Snap)
sudo snap install --classic heroku
```

2. **Login to Heroku**:
```bash
heroku login
```

3. **Navigate to backend directory**:
```bash
cd diagnostic-repair-app/backend
```

4. **Create a new Heroku app**:
```bash
heroku create your-diagnostic-app-backend
```

5. **Set environment variables**:
```bash
heroku config:set NODE_ENV=production
heroku config:set PORT=3000
# Add any other environment variables you need
```

6. **Deploy to Heroku**:
```bash
git init  # if not already a git repo
git add .
git commit -m "Initial backend deployment"
heroku git:remote -a your-diagnostic-app-backend
git push heroku main
```

7. **Verify deployment**:
```bash
heroku logs --tail
heroku open
```

8. **Scale dynos** (if needed):
```bash
heroku ps:scale web=1
```

#### Post-Deployment
- Your backend will be available at: `https://your-diagnostic-app-backend.herokuapp.com`
- Update this URL in your Flutter frontend configuration

---

### AWS Deployment

#### Using AWS Elastic Beanstalk

1. **Install AWS CLI and EB CLI**:
```bash
pip install awscli awsebcli
```

2. **Configure AWS credentials**:
```bash
aws configure
```

3. **Initialize Elastic Beanstalk**:
```bash
cd diagnostic-repair-app/backend
eb init -p node.js your-diagnostic-app
```

4. **Create environment and deploy**:
```bash
eb create diagnostic-app-env
eb deploy
```

5. **Set environment variables**:
```bash
eb setenv NODE_ENV=production PORT=8080
```

6. **Open application**:
```bash
eb open
```

#### Using EC2 (Manual Setup)

1. **Launch EC2 instance** (Ubuntu 22.04 recommended)

2. **Connect to instance**:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Node.js**:
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

4. **Install PM2** (process manager):
```bash
sudo npm install -g pm2
```

5. **Clone and setup application**:
```bash
git clone <your-repo-url>
cd diagnostic-repair-app/backend
npm install
```

6. **Create .env file**:
```bash
nano .env
# Add your environment variables
```

7. **Start application with PM2**:
```bash
pm2 start server.js --name diagnostic-backend
pm2 save
pm2 startup
```

8. **Setup Nginx as reverse proxy**:
```bash
sudo apt-get install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/diagnostic-app

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/diagnostic-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. **Setup SSL with Let's Encrypt**:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

### DigitalOcean Deployment

#### Using App Platform

1. **Create a new app** in DigitalOcean dashboard

2. **Connect your GitHub repository**

3. **Configure build settings**:
   - Build Command: `npm install`
   - Run Command: `npm start`
   - HTTP Port: 3000

4. **Set environment variables** in app settings

5. **Deploy** and get your app URL

---

## Frontend Deployment

### Firebase Hosting

#### Prerequisites
- Firebase account
- Firebase CLI installed
- Flutter project built for web

#### Step-by-Step Instructions

1. **Install Firebase CLI**:
```bash
npm install -g firebase-tools
```

2. **Login to Firebase**:
```bash
firebase login
```

3. **Initialize Firebase in your project**:
```bash
cd diagnostic-repair-app/frontend
firebase init
```

Select:
- ✅ Hosting
- ✅ Firestore (optional)

4. **Configure firebase.json**:
```json
{
  "hosting": {
    "public": "build/web",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

5. **Update backend URL in Flutter app**:
```dart
// lib/main.dart
apiService = ApiService(baseUrl: 'https://your-backend-url.herokuapp.com/api');
socketService = SocketService(serverUrl: 'https://your-backend-url.herokuapp.com');
```

6. **Build Flutter web app**:
```bash
flutter build web --release
```

7. **Deploy to Firebase**:
```bash
firebase deploy
```

8. **Your app will be available at**:
```
https://your-project-id.web.app
```

#### Custom Domain Setup

1. **Add custom domain in Firebase Console**:
   - Go to Hosting → Add custom domain
   - Follow DNS configuration instructions

2. **Update DNS records** with your domain provider

---

### Netlify (Alternative)

1. **Install Netlify CLI**:
```bash
npm install -g netlify-cli
```

2. **Build Flutter web**:
```bash
flutter build web --release
```

3. **Deploy**:
```bash
netlify deploy --dir=build/web --prod
```

---

## Firebase Cloud Messaging

### Setup FCM for Push Notifications

1. **Create Firebase project** at https://console.firebase.google.com

2. **Add your Flutter app** to the project

3. **Download configuration files**:
   - `google-services.json` for Android
   - `GoogleService-Info.plist` for iOS

4. **Add to Flutter project**:
```
android/app/google-services.json
ios/Runner/GoogleService-Info.plist
```

5. **Install FCM package**:
```yaml
# pubspec.yaml
dependencies:
  firebase_messaging: ^14.6.0
```

6. **Initialize FCM in Flutter**:
```dart
// lib/services/fcm_service.dart
import 'package:firebase_messaging/firebase_messaging.dart';

class FCMService {
  final FirebaseMessaging _fcm = FirebaseMessaging.instance;

  Future<void> init() async {
    // Request permission
    NotificationSettings settings = await _fcm.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );

    // Get FCM token
    String? token = await _fcm.getToken();
    print('FCM Token: $token');

    // Listen to messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('Got a message: ${message.notification?.title}');
    });
  }
}
```

7. **Send notifications from backend**:
```javascript
// Backend - routes/notifications.js
const admin = require('firebase-admin');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

async function sendNotification(token, title, body) {
  const message = {
    notification: { title, body },
    token: token
  };

  try {
    const response = await admin.messaging().send(message);
    console.log('Successfully sent message:', response);
  } catch (error) {
    console.log('Error sending message:', error);
  }
}
```

---

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in backend directory:

```bash
# Server Configuration
NODE_ENV=production
PORT=3000

# Database (if using)
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=diagnostic_db
DB_USER=your-username
DB_PASSWORD=your-password

# Firebase Admin SDK
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=your-service-account-email
FIREBASE_PRIVATE_KEY="your-private-key"

# FCM Server Key
FCM_SERVER_KEY=your-fcm-server-key

# CORS Origins
ALLOWED_ORIGINS=https://your-frontend-domain.com

# API Keys (if needed)
API_SECRET_KEY=your-secret-key
```

### Frontend Environment Configuration

Create environment-specific configurations:

```dart
// lib/config/environment.dart
class Environment {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://localhost:3000/api',
  );

  static const String socketUrl = String.fromEnvironment(
    'SOCKET_URL',
    defaultValue: 'http://localhost:3000',
  );
}
```

Build with environment variables:
```bash
flutter build web --dart-define=API_URL=https://your-api.herokuapp.com/api
```

---

## Monitoring and Maintenance

### Backend Monitoring

1. **Heroku Logs**:
```bash
heroku logs --tail --app your-app-name
```

2. **Set up logging service** (e.g., Papertrail, Loggly)

3. **Monitor metrics**:
```bash
heroku ps --app your-app-name
```

### Frontend Monitoring

1. **Firebase Analytics** - Track user behavior
2. **Crashlytics** - Monitor app crashes
3. **Performance Monitoring** - Track app performance

---

## Troubleshooting

### Common Issues

1. **CORS errors**:
   - Ensure backend CORS is configured for your frontend domain
   - Check firewall/security group settings

2. **Socket.IO connection issues**:
   - Verify WebSocket support on hosting platform
   - Check for proxy configuration issues

3. **Build failures**:
   - Ensure all dependencies are installed
   - Check Node.js/Flutter versions

4. **Environment variables not loading**:
   - Verify .env file is in correct location
   - Check environment variable names

---

## Security Checklist

- [ ] Use HTTPS for all communications
- [ ] Implement authentication/authorization
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Implement CORS properly
- [ ] Keep dependencies updated
- [ ] Use secure headers
- [ ] Implement input validation
- [ ] Enable SSL/TLS
- [ ] Regular security audits

---

**Need help?** Contact the development team for assistance.
