const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const util = require('util');
const fs = require('fs').promises;
const path = require('path');

const execPromise = util.promisify(exec);

// Flash Android firmware via Fastboot
router.post('/android/flash', async (req, res) => {
  try {
    const { deviceId, firmwarePath, partition } = req.body;

    if (!deviceId || !firmwarePath || !partition) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: deviceId, firmwarePath, partition'
      });
    }

    // Check if firmware file exists
    try {
      await fs.access(firmwarePath);
    } catch (error) {
      return res.status(404).json({
        success: false,
        error: 'Firmware file not found'
      });
    }

    const io = req.app.get('io');
    
    // Emit start event
    io.emit('flash-started', { deviceId, partition });

    // Flash firmware using fastboot
    const command = `fastboot -s ${deviceId} flash ${partition} ${firmwarePath}`;
    
    exec(command, (error, stdout, stderr) => {
      if (error) {
        io.emit('flash-failed', { 
          deviceId, 
          partition, 
          error: error.message,
          stderr 
        });
        return;
      }

      io.emit('flash-progress', { 
        deviceId, 
        partition, 
        output: stdout 
      });

      io.emit('flash-completed', { 
        deviceId, 
        partition 
      });
    });

    res.json({ 
      success: true, 
      message: 'Firmware flashing started',
      deviceId,
      partition
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Flash Android full ROM
router.post('/android/flash-all', async (req, res) => {
  try {
    const { deviceId, firmwareDir } = req.body;

    if (!deviceId || !firmwareDir) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: deviceId, firmwareDir'
      });
    }

    // Check if firmware directory exists
    try {
      await fs.access(firmwareDir);
    } catch (error) {
      return res.status(404).json({
        success: false,
        error: 'Firmware directory not found'
      });
    }

    const io = req.app.get('io');
    
    // Emit start event
    io.emit('flash-all-started', { deviceId });

    // Look for flash-all script
    const scriptPath = path.join(firmwareDir, 'flash-all.sh');
    let command;

    try {
      await fs.access(scriptPath);
      command = `cd ${firmwareDir} && bash flash-all.sh`;
    } catch (error) {
      // Fallback to manual flashing
      command = `cd ${firmwareDir} && fastboot -s ${deviceId} flashall`;
    }

    exec(command, { maxBuffer: 1024 * 1024 * 10 }, (error, stdout, stderr) => {
      if (error) {
        io.emit('flash-all-failed', { 
          deviceId, 
          error: error.message,
          stderr 
        });
        return;
      }

      io.emit('flash-all-progress', { 
        deviceId, 
        output: stdout 
      });

      io.emit('flash-all-completed', { deviceId });
    });

    res.json({ 
      success: true, 
      message: 'Full ROM flashing started',
      deviceId
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Flash iOS firmware (using idevicerestore)
router.post('/ios/restore', async (req, res) => {
  try {
    const { deviceId, ipswPath } = req.body;

    if (!deviceId || !ipswPath) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields: deviceId, ipswPath'
      });
    }

    // Check if IPSW file exists
    try {
      await fs.access(ipswPath);
    } catch (error) {
      return res.status(404).json({
        success: false,
        error: 'IPSW file not found'
      });
    }

    const io = req.app.get('io');
    
    // Emit start event
    io.emit('restore-started', { deviceId });

    // Restore using idevicerestore
    const command = `idevicerestore -u ${deviceId} ${ipswPath}`;
    
    exec(command, { maxBuffer: 1024 * 1024 * 50 }, (error, stdout, stderr) => {
      if (error) {
        io.emit('restore-failed', { 
          deviceId, 
          error: error.message,
          stderr 
        });
        return;
      }

      io.emit('restore-progress', { 
        deviceId, 
        output: stdout 
      });

      io.emit('restore-completed', { deviceId });
    });

    res.json({ 
      success: true, 
      message: 'iOS restore started',
      deviceId
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Check Android device in fastboot mode
router.get('/android/fastboot-devices', async (req, res) => {
  try {
    const { stdout } = await execPromise('fastboot devices');
    const devices = stdout.trim().split('\n')
      .filter(line => line)
      .map(line => {
        const [id, status] = line.split('\t');
        return { id, status };
      });

    res.json({
      success: true,
      count: devices.length,
      devices
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get flashing progress
router.get('/progress/:deviceId', (req, res) => {
  // This would typically query a database or cache for progress
  res.json({
    success: true,
    message: 'Use Socket.IO for real-time progress updates'
  });
});

// Unlock bootloader (Android)
router.post('/android/:deviceId/unlock-bootloader', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const { stdout } = await execPromise(`fastboot -s ${deviceId} oem unlock`);
    
    res.json({ 
      success: true, 
      message: 'Bootloader unlock command sent. Follow on-screen instructions.',
      output: stdout
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Lock bootloader (Android)
router.post('/android/:deviceId/lock-bootloader', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const { stdout } = await execPromise(`fastboot -s ${deviceId} oem lock`);
    
    res.json({ 
      success: true, 
      message: 'Bootloader lock command sent',
      output: stdout
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Erase partition (Android)
router.post('/android/:deviceId/erase', async (req, res) => {
  try {
    const { deviceId } = req.params;
    const { partition } = req.body;

    if (!partition) {
      return res.status(400).json({
        success: false,
        error: 'Missing required field: partition'
      });
    }

    const { stdout } = await execPromise(`fastboot -s ${deviceId} erase ${partition}`);
    
    res.json({ 
      success: true, 
      message: `Partition ${partition} erased`,
      output: stdout
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
