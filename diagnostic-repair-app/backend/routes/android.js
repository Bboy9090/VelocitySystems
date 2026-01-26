const express = require('express');
const router = express.Router();
const adb = require('adbkit');
const client = adb.createClient();

// List connected Android devices
router.get('/devices', async (req, res) => {
  try {
    const devices = await client.listDevices();
    const deviceList = devices.map(device => ({
      id: device.id,
      type: device.type
    }));

    res.json({
      success: true,
      count: deviceList.length,
      devices: deviceList
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get device information
router.get('/devices/:deviceId/info', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const properties = await client.getProperties(deviceId);
    const deviceInfo = {
      id: deviceId,
      manufacturer: properties['ro.product.manufacturer'],
      model: properties['ro.product.model'],
      brand: properties['ro.product.brand'],
      androidVersion: properties['ro.build.version.release'],
      sdkVersion: properties['ro.build.version.sdk'],
      serialNumber: properties['ro.serialno'],
      buildId: properties['ro.build.id']
    };

    res.json({ success: true, device: deviceInfo });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get battery information
router.get('/devices/:deviceId/battery', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    const output = await client.shell(deviceId, 'dumpsys battery');
    const batteryData = await streamToString(output);
    
    const battery = parseBatteryInfo(batteryData);

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
    const { filter, lines } = req.query;
    
    let command = 'logcat -d';
    if (lines) command += ` -t ${lines}`;
    if (filter) command += ` | grep "${filter}"`;
    
    const output = await client.shell(deviceId, command);
    const logs = await streamToString(output);

    res.json({ 
      success: true, 
      logs: logs.split('\n').filter(line => line.trim())
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

    // Battery health
    const batteryOutput = await client.shell(deviceId, 'dumpsys battery');
    const batteryData = await streamToString(batteryOutput);
    diagnostics.battery = parseBatteryInfo(batteryData);

    // Storage info
    const storageOutput = await client.shell(deviceId, 'df');
    const storageData = await streamToString(storageOutput);
    diagnostics.storage = parseStorageInfo(storageData);

    // Memory info
    const memoryOutput = await client.shell(deviceId, 'cat /proc/meminfo');
    const memoryData = await streamToString(memoryOutput);
    diagnostics.memory = parseMemoryInfo(memoryData);

    // CPU info
    const cpuOutput = await client.shell(deviceId, 'cat /proc/cpuinfo');
    const cpuData = await streamToString(cpuOutput);
    diagnostics.cpu = parseCpuInfo(cpuData);

    // Network info
    const networkOutput = await client.shell(deviceId, 'ip addr');
    const networkData = await streamToString(networkOutput);
    diagnostics.network = parseNetworkInfo(networkData);

    // Complete diagnostics
    io.emit('diagnostics-completed', { deviceId, diagnostics });

    res.json({ success: true, diagnostics });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Enter Fastboot mode
router.post('/devices/:deviceId/fastboot', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    await client.shell(deviceId, 'reboot bootloader');
    
    res.json({ 
      success: true, 
      message: 'Device rebooting to fastboot mode' 
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Enter Recovery mode
router.post('/devices/:deviceId/recovery', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    await client.shell(deviceId, 'reboot recovery');
    
    res.json({ 
      success: true, 
      message: 'Device rebooting to recovery mode' 
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Reboot device
router.post('/devices/:deviceId/reboot', async (req, res) => {
  try {
    const { deviceId } = req.params;
    
    await client.shell(deviceId, 'reboot');
    
    res.json({ 
      success: true, 
      message: 'Device rebooting' 
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Helper functions
function streamToString(stream) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    stream.on('data', chunk => chunks.push(chunk));
    stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    stream.on('error', reject);
  });
}

function parseBatteryInfo(data) {
  const lines = data.split('\n');
  const battery = {};
  
  lines.forEach(line => {
    if (line.includes('level:')) {
      battery.level = parseInt(line.split(':')[1].trim());
    }
    if (line.includes('health:')) {
      battery.health = line.split(':')[1].trim();
    }
    if (line.includes('status:')) {
      battery.status = line.split(':')[1].trim();
    }
    if (line.includes('temperature:')) {
      battery.temperature = parseInt(line.split(':')[1].trim()) / 10;
    }
    if (line.includes('voltage:')) {
      battery.voltage = parseInt(line.split(':')[1].trim());
    }
  });
  
  return battery;
}

function parseStorageInfo(data) {
  const lines = data.split('\n').filter(line => line.includes('/data') || line.includes('/storage'));
  const storage = { partitions: [] };
  
  lines.forEach(line => {
    const parts = line.trim().split(/\s+/);
    if (parts.length >= 6) {
      storage.partitions.push({
        filesystem: parts[0],
        size: parts[1],
        used: parts[2],
        available: parts[3],
        usagePercent: parts[4],
        mountPoint: parts[5]
      });
    }
  });
  
  return storage;
}

function parseMemoryInfo(data) {
  const lines = data.split('\n');
  const memory = {};
  
  lines.forEach(line => {
    if (line.includes('MemTotal:')) {
      memory.total = line.split(':')[1].trim();
    }
    if (line.includes('MemFree:')) {
      memory.free = line.split(':')[1].trim();
    }
    if (line.includes('MemAvailable:')) {
      memory.available = line.split(':')[1].trim();
    }
  });
  
  return memory;
}

function parseCpuInfo(data) {
  const lines = data.split('\n');
  const processors = [];
  let currentProcessor = {};
  
  lines.forEach(line => {
    if (line.includes('processor')) {
      if (Object.keys(currentProcessor).length > 0) {
        processors.push(currentProcessor);
      }
      currentProcessor = { id: line.split(':')[1].trim() };
    }
    if (line.includes('model name')) {
      currentProcessor.model = line.split(':')[1].trim();
    }
    if (line.includes('cpu MHz')) {
      currentProcessor.mhz = line.split(':')[1].trim();
    }
  });
  
  if (Object.keys(currentProcessor).length > 0) {
    processors.push(currentProcessor);
  }
  
  return { processors, count: processors.length };
}

function parseNetworkInfo(data) {
  const interfaces = [];
  const lines = data.split('\n');
  let currentInterface = null;
  
  lines.forEach(line => {
    if (line.match(/^\d+:/)) {
      if (currentInterface) interfaces.push(currentInterface);
      const name = line.split(':')[1].trim().split(':')[0];
      currentInterface = { name, addresses: [] };
    } else if (line.includes('inet') && currentInterface) {
      const addr = line.trim().split(/\s+/)[1];
      currentInterface.addresses.push(addr);
    }
  });
  
  if (currentInterface) interfaces.push(currentInterface);
  
  return { interfaces };
}

module.exports = router;
