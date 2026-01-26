const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

// List connected iOS devices
router.get('/devices', async (req, res) => {
  try {
    const { stdout } = await execPromise('idevice_id -l');
    const deviceIds = stdout.trim().split('\n').filter(id => id);

    const devices = [];
    for (const deviceId of deviceIds) {
      if (deviceId) {
        devices.push({
          id: deviceId,
          type: 'device'
        });
      }
    }

    res.json({
      success: true,
      count: devices.length,
      devices
    });
  } catch (error) {
    res.status(500).json({ 
      success: false, 
      error: error.message,
      note: 'Make sure libimobiledevice is installed'
    });
  }
});

// Get device information
router.get('/devices/:deviceId/info', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const { stdout } = await execPromise(`ideviceinfo -u ${deviceId}`);
    const deviceInfo = parseDeviceInfo(stdout);

    res.json({ success: true, device: deviceInfo });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get battery information
router.get('/devices/:deviceId/battery', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const { stdout } = await execPromise(`ideviceinfo -u ${deviceId} -k BatteryCurrentCapacity`);
    const level = parseInt(stdout.trim());
    
    const { stdout: isCharging } = await execPromise(`ideviceinfo -u ${deviceId} -k BatteryIsCharging`).catch(() => ({ stdout: 'false' }));
    
    const battery = {
      level,
      isCharging: isCharging.trim().toLowerCase() === 'true',
      timestamp: new Date().toISOString()
    };

    // Emit real-time update
    const io = req.app.get('io');
    io.emit('battery-update', { deviceId, battery });

    res.json({ success: true, battery });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get system logs
router.get('/devices/:deviceId/logs', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const { stdout } = await execPromise(`idevicesyslog -u ${deviceId} | head -n 100`);
    const logs = stdout.split('\n').filter(line => line.trim());

    res.json({ 
      success: true, 
      logs
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Run hardware diagnostics
router.post('/devices/:deviceId/diagnostics', async (req, res) => {
  try {
    const { deviceId } = req.params;
    const io = req.app.get('io');

    // Start diagnostics
    io.emit('diagnostics-started', { deviceId });

    const diagnostics = {};

    // Get device info
    const { stdout: infoOutput } = await execPromise(`ideviceinfo -u ${deviceId}`);
    const deviceInfo = parseDeviceInfo(infoOutput);
    
    diagnostics.device = deviceInfo;

    // Battery info
    try {
      const { stdout: batteryLevel } = await execPromise(`ideviceinfo -u ${deviceId} -k BatteryCurrentCapacity`);
      diagnostics.battery = {
        level: parseInt(batteryLevel.trim()),
        health: 'Unknown' // iOS doesn't expose battery health via libimobiledevice
      };
    } catch (e) {
      diagnostics.battery = { error: 'Unable to retrieve battery info' };
    }

    // Storage info
    try {
      const { stdout: diskTotal } = await execPromise(`ideviceinfo -u ${deviceId} -k TotalDiskCapacity`);
      const { stdout: diskFree } = await execPromise(`ideviceinfo -u ${deviceId} -k TotalSystemAvailable`);
      
      diagnostics.storage = {
        total: parseInt(diskTotal.trim()),
        available: parseInt(diskFree.trim()),
        used: parseInt(diskTotal.trim()) - parseInt(diskFree.trim())
      };
    } catch (e) {
      diagnostics.storage = { error: 'Unable to retrieve storage info' };
    }

    // Network info
    try {
      const { stdout: wifiAddress } = await execPromise(`ideviceinfo -u ${deviceId} -k WiFiAddress`).catch(() => ({ stdout: '' }));
      diagnostics.network = {
        wifiAddress: wifiAddress.trim() || 'Not available'
      };
    } catch (e) {
      diagnostics.network = { error: 'Unable to retrieve network info' };
    }

    // Complete diagnostics
    io.emit('diagnostics-completed', { deviceId, diagnostics });

    res.json({ success: true, diagnostics });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Enter Recovery mode
router.post('/devices/:deviceId/recovery', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    await execPromise(`ideviceenterrecovery ${deviceId}`);
    
    res.json({ 
      success: true, 
      message: 'Device entering recovery mode' 
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Enter DFU mode (requires user interaction)
router.post('/devices/:deviceId/dfu', async (req, res) => {
  try {
    res.json({ 
      success: true, 
      message: 'DFU mode requires manual steps',
      instructions: [
        '1. Connect device to computer',
        '2. Press and hold Power button for 3 seconds',
        '3. While holding Power, press and hold Volume Down for 10 seconds',
        '4. Release Power button but keep holding Volume Down for 5 more seconds',
        '5. Device should be in DFU mode (screen should be black)'
      ]
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Reboot device
router.post('/devices/:deviceId/reboot', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    await execPromise(`idevicediagnostics -u ${deviceId} restart`);
    
    res.json({ 
      success: true, 
      message: 'Device rebooting' 
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Backup device
router.post('/devices/:deviceId/backup', async (req, res) => {
  try {
    const { deviceId } = req.params;
    const backupPath = `/tmp/ios_backup_${deviceId}_${Date.now()}`;
    
    // Start backup in background
    exec(`idevicebackup2 -u ${deviceId} backup ${backupPath}`, (error, stdout, stderr) => {
      const io = req.app.get('io');
      if (error) {
        io.emit('backup-failed', { deviceId, error: error.message });
      } else {
        io.emit('backup-completed', { deviceId, path: backupPath });
      }
    });
    
    res.json({ 
      success: true, 
      message: 'Backup started',
      backupPath
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Helper function to parse device info
function parseDeviceInfo(output) {
  const info = {};
  const lines = output.split('\n');
  
  lines.forEach(line => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length > 0) {
      const value = valueParts.join(':').trim();
      const cleanKey = key.trim();
      
      switch (cleanKey) {
        case 'DeviceName':
          info.name = value;
          break;
        case 'ProductType':
          info.model = value;
          break;
        case 'ProductVersion':
          info.version = value;
          break;
        case 'BuildVersion':
          info.buildVersion = value;
          break;
        case 'SerialNumber':
          info.serialNumber = value;
          break;
        case 'UniqueDeviceID':
          info.udid = value;
          break;
        case 'PhoneNumber':
          info.phoneNumber = value;
          break;
        case 'WiFiAddress':
          info.wifiAddress = value;
          break;
        case 'BluetoothAddress':
          info.bluetoothAddress = value;
          break;
      }
    }
  });
  
  return info;
}

module.exports = router;
