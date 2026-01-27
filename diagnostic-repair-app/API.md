# API Documentation

Complete API reference for the Diagnostic & Repair App backend.

## Base URL
```
http://localhost:3000/api
```

---

## 🎫 Repair Tickets API

### GET /tickets
Get all repair tickets with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (open, in-progress, waiting-parts, completed, cancelled)
- `customerId` (optional): Filter by customer ID

**Response:**
```json
{
  "success": true,
  "count": 2,
  "tickets": [
    {
      "id": "uuid",
      "ticketNumber": "TKT-1234567890",
      "customer": {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
      },
      "device": {
        "type": "android",
        "manufacturer": "Samsung",
        "model": "Galaxy S21",
        "serialNumber": "ABC123",
        "imei": "123456789012345"
      },
      "issue": {
        "description": "Screen not responding",
        "category": "display",
        "severity": "high"
      },
      "status": "open",
      "priority": "normal",
      "estimatedCost": 0,
      "actualCost": 0,
      "diagnostics": {},
      "repairHistory": [],
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

---

### GET /tickets/:id
Get a single repair ticket by ID.

**Response:**
```json
{
  "success": true,
  "ticket": { ... }
}
```

---

### POST /tickets
Create a new repair ticket.

**Request Body:**
```json
{
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "device": {
    "type": "android",
    "manufacturer": "Samsung",
    "model": "Galaxy S21",
    "serialNumber": "ABC123",
    "imei": "123456789012345"
  },
  "issue": {
    "description": "Screen not responding",
    "category": "display",
    "severity": "high"
  },
  "priority": "normal"
}
```

**Response:**
```json
{
  "success": true,
  "ticket": { ... }
}
```

---

### PUT /tickets/:id
Update an existing ticket.

**Request Body:**
```json
{
  "estimatedCost": 150,
  "status": "in-progress"
}
```

**Response:**
```json
{
  "success": true,
  "ticket": { ... }
}
```

---

### PATCH /tickets/:id/status
Update ticket status with optional note.

**Request Body:**
```json
{
  "status": "completed",
  "note": "Repair completed successfully"
}
```

**Response:**
```json
{
  "success": true,
  "ticket": { ... }
}
```

---

### POST /tickets/:id/diagnostics
Add diagnostic data to a ticket.

**Request Body:**
```json
{
  "battery": {
    "level": 85,
    "health": "good"
  },
  "storage": {
    "total": "128GB",
    "used": "45GB"
  }
}
```

**Response:**
```json
{
  "success": true,
  "ticket": { ... }
}
```

---

### DELETE /tickets/:id
Delete a ticket.

**Response:**
```json
{
  "success": true,
  "ticket": { ... }
}
```

---

## 🤖 Android Diagnostics API

### GET /android/devices
List all connected Android devices.

**Response:**
```json
{
  "success": true,
  "count": 1,
  "devices": [
    {
      "id": "ABC123",
      "type": "device"
    }
  ]
}
```

---

### GET /android/devices/:deviceId/info
Get device information.

**Response:**
```json
{
  "success": true,
  "device": {
    "id": "ABC123",
    "manufacturer": "Samsung",
    "model": "Galaxy S21",
    "brand": "samsung",
    "androidVersion": "12",
    "sdkVersion": "31",
    "serialNumber": "ABC123",
    "buildId": "SP1A.210812.016"
  }
}
```

---

### GET /android/devices/:deviceId/battery
Get battery information.

**Response:**
```json
{
  "success": true,
  "battery": {
    "level": 85,
    "health": "2",
    "status": "2",
    "temperature": 30.5,
    "voltage": 4200
  }
}
```

---

### GET /android/devices/:deviceId/logs
Get system logs.

**Query Parameters:**
- `filter` (optional): Filter logs by text
- `lines` (optional): Number of lines to retrieve

**Response:**
```json
{
  "success": true,
  "logs": [
    "log line 1",
    "log line 2"
  ]
}
```

---

### POST /android/devices/:deviceId/diagnostics
Run full hardware diagnostics.

**Response:**
```json
{
  "success": true,
  "diagnostics": {
    "battery": { ... },
    "storage": { ... },
    "memory": { ... },
    "cpu": { ... },
    "network": { ... }
  }
}
```

---

### POST /android/devices/:deviceId/fastboot
Reboot device to fastboot mode.

**Response:**
```json
{
  "success": true,
  "message": "Device rebooting to fastboot mode"
}
```

---

### POST /android/devices/:deviceId/recovery
Reboot device to recovery mode.

**Response:**
```json
{
  "success": true,
  "message": "Device rebooting to recovery mode"
}
```

---

### POST /android/devices/:deviceId/reboot
Reboot device normally.

**Response:**
```json
{
  "success": true,
  "message": "Device rebooting"
}
```

---

## 🍎 iOS Diagnostics API

### GET /ios/devices
List all connected iOS devices.

**Response:**
```json
{
  "success": true,
  "count": 1,
  "devices": [
    {
      "id": "00001111-000A1B2C3D4E5F6G",
      "type": "device"
    }
  ]
}
```

---

### GET /ios/devices/:deviceId/info
Get device information.

**Response:**
```json
{
  "success": true,
  "device": {
    "name": "John's iPhone",
    "model": "iPhone13,2",
    "version": "16.0",
    "buildVersion": "20A362",
    "serialNumber": "ABC123",
    "udid": "00001111-000A1B2C3D4E5F6G",
    "phoneNumber": "+1234567890",
    "wifiAddress": "aa:bb:cc:dd:ee:ff",
    "bluetoothAddress": "ff:ee:dd:cc:bb:aa"
  }
}
```

---

### GET /ios/devices/:deviceId/battery
Get battery information.

**Response:**
```json
{
  "success": true,
  "battery": {
    "level": 85,
    "isCharging": true,
    "timestamp": "2024-01-01T00:00:00.000Z"
  }
}
```

---

### GET /ios/devices/:deviceId/logs
Get system logs.

**Response:**
```json
{
  "success": true,
  "logs": [
    "log line 1",
    "log line 2"
  ]
}
```

---

### POST /ios/devices/:deviceId/diagnostics
Run full hardware diagnostics.

**Response:**
```json
{
  "success": true,
  "diagnostics": {
    "device": { ... },
    "battery": { ... },
    "storage": { ... },
    "network": { ... }
  }
}
```

---

### POST /ios/devices/:deviceId/recovery
Enter recovery mode.

**Response:**
```json
{
  "success": true,
  "message": "Device entering recovery mode"
}
```

---

### POST /ios/devices/:deviceId/dfu
Get DFU mode instructions.

**Response:**
```json
{
  "success": true,
  "message": "DFU mode requires manual steps",
  "instructions": [
    "1. Connect device to computer",
    "2. Press and hold Power button for 3 seconds",
    "..."
  ]
}
```

---

### POST /ios/devices/:deviceId/reboot
Reboot device.

**Response:**
```json
{
  "success": true,
  "message": "Device rebooting"
}
```

---

### POST /ios/devices/:deviceId/backup
Create device backup.

**Response:**
```json
{
  "success": true,
  "message": "Backup started",
  "backupPath": "/tmp/ios_backup_..."
}
```

---

## 💾 Firmware Flashing API

### POST /firmware/android/flash
Flash a single partition on Android device.

**Request Body:**
```json
{
  "deviceId": "ABC123",
  "firmwarePath": "/path/to/boot.img",
  "partition": "boot"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Firmware flashing started",
  "deviceId": "ABC123",
  "partition": "boot"
}
```

---

### POST /firmware/android/flash-all
Flash complete ROM on Android device.

**Request Body:**
```json
{
  "deviceId": "ABC123",
  "firmwareDir": "/path/to/firmware"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Full ROM flashing started",
  "deviceId": "ABC123"
}
```

---

### POST /firmware/ios/restore
Restore iOS firmware using IPSW file.

**Request Body:**
```json
{
  "deviceId": "00001111-000A1B2C3D4E5F6G",
  "ipswPath": "/path/to/firmware.ipsw"
}
```

**Response:**
```json
{
  "success": true,
  "message": "iOS restore started",
  "deviceId": "00001111-000A1B2C3D4E5F6G"
}
```

---

### GET /firmware/android/fastboot-devices
List devices in fastboot mode.

**Response:**
```json
{
  "success": true,
  "count": 1,
  "devices": [
    {
      "id": "ABC123",
      "status": "fastboot"
    }
  ]
}
```

---

### POST /firmware/android/:deviceId/unlock-bootloader
Unlock device bootloader.

**Response:**
```json
{
  "success": true,
  "message": "Bootloader unlock command sent. Follow on-screen instructions.",
  "output": "..."
}
```

---

### POST /firmware/android/:deviceId/lock-bootloader
Lock device bootloader.

**Response:**
```json
{
  "success": true,
  "message": "Bootloader lock command sent",
  "output": "..."
}
```

---

### POST /firmware/android/:deviceId/erase
Erase a partition.

**Request Body:**
```json
{
  "partition": "cache"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Partition cache erased",
  "output": "..."
}
```

---

## 🔌 Socket.IO Events

### Client Events

#### subscribe-ticket
Subscribe to updates for a specific ticket.

**Emit:**
```javascript
socket.emit('subscribe-ticket', ticketId);
```

---

### Server Events

#### ticket-created
Emitted when a new ticket is created.

**Payload:**
```json
{
  "id": "uuid",
  "ticketNumber": "TKT-1234567890",
  ...
}
```

---

#### ticket-updated
Emitted when a ticket is updated.

**Payload:**
```json
{
  "id": "uuid",
  "ticketNumber": "TKT-1234567890",
  ...
}
```

---

#### ticket-status-changed
Emitted when ticket status changes.

**Payload:**
```json
{
  "ticketId": "uuid",
  "status": "completed",
  "note": "Repair completed"
}
```

---

#### diagnostics-started
Emitted when diagnostics start.

**Payload:**
```json
{
  "deviceId": "ABC123"
}
```

---

#### diagnostics-completed
Emitted when diagnostics complete.

**Payload:**
```json
{
  "deviceId": "ABC123",
  "diagnostics": { ... }
}
```

---

#### battery-update
Real-time battery level updates.

**Payload:**
```json
{
  "deviceId": "ABC123",
  "battery": {
    "level": 85,
    "health": "good"
  }
}
```

---

#### flash-started
Emitted when firmware flash starts.

**Payload:**
```json
{
  "deviceId": "ABC123",
  "partition": "boot"
}
```

---

#### flash-progress
Emitted during firmware flash progress.

**Payload:**
```json
{
  "deviceId": "ABC123",
  "partition": "boot",
  "output": "Sending 'boot' (12345 KB)..."
}
```

---

#### flash-completed
Emitted when firmware flash completes.

**Payload:**
```json
{
  "deviceId": "ABC123",
  "partition": "boot"
}
```

---

#### flash-failed
Emitted when firmware flash fails.

**Payload:**
```json
{
  "deviceId": "ABC123",
  "partition": "boot",
  "error": "Error message",
  "stderr": "Error details"
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Rate Limiting

Currently not implemented. Recommended to add rate limiting in production.

---

## Authentication

Currently not implemented. Recommended to add authentication in production using JWT or OAuth2.

---

## CORS

CORS is enabled for all origins in development. In production, configure allowed origins in environment variables.

---

**For additional support or questions, contact the development team.**
