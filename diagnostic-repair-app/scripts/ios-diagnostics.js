#!/usr/bin/env node

/**
 * iOS Diagnostic Script
 * Uses libimobiledevice tools to run diagnostics on connected iOS devices
 */

const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

async function listDevices() {
  try {
    console.log('Checking for connected iOS devices...\n');
    const { stdout } = await execPromise('idevice_id -l');
    const deviceIds = stdout.trim().split('\n').filter(id => id);
    
    if (deviceIds.length === 0) {
      console.log('No iOS devices connected.');
      return [];
    }
    
    console.log('Connected iOS devices:');
    deviceIds.forEach((id, index) => {
      console.log(`${index + 1}. ${id}`);
    });
    
    return deviceIds;
  } catch (error) {
    console.error('Error listing devices:', error.message);
    console.error('Make sure libimobiledevice is installed:');
    console.error('  macOS: brew install libimobiledevice');
    console.error('  Linux: apt-get install libimobiledevice-tools');
    return [];
  }
}

async function getDeviceInfo(deviceId) {
  try {
    console.log(`\n=== Device Information ===`);
    const { stdout } = await execPromise(`ideviceinfo -u ${deviceId}`);
    
    const info = parseDeviceInfo(stdout);
    console.log(`Device Name: ${info.name || 'N/A'}`);
    console.log(`Model: ${info.model || 'N/A'}`);
    console.log(`iOS Version: ${info.version || 'N/A'}`);
    console.log(`Build Version: ${info.buildVersion || 'N/A'}`);
    console.log(`Serial Number: ${info.serialNumber || 'N/A'}`);
    console.log(`UDID: ${info.udid || 'N/A'}`);
    console.log(`WiFi Address: ${info.wifiAddress || 'N/A'}`);
    
    return info;
  } catch (error) {
    console.error('Error getting device info:', error.message);
  }
}

async function getBatteryInfo(deviceId) {
  try {
    console.log(`\n=== Battery Information ===`);
    
    try {
      const { stdout: level } = await execPromise(`ideviceinfo -u ${deviceId} -k BatteryCurrentCapacity`);
      console.log(`Battery Level: ${level.trim()}%`);
    } catch (e) {
      console.log('Battery Level: Unable to retrieve');
    }
    
    try {
      const { stdout: isCharging } = await execPromise(`ideviceinfo -u ${deviceId} -k BatteryIsCharging`);
      console.log(`Is Charging: ${isCharging.trim()}`);
    } catch (e) {
      console.log('Charging Status: Unable to retrieve');
    }
  } catch (error) {
    console.error('Error getting battery info:', error.message);
  }
}

async function getStorageInfo(deviceId) {
  try {
    console.log(`\n=== Storage Information ===`);
    
    try {
      const { stdout: totalDisk } = await execPromise(`ideviceinfo -u ${deviceId} -k TotalDiskCapacity`);
      const totalGB = (parseInt(totalDisk.trim()) / 1073741824).toFixed(2);
      console.log(`Total Capacity: ${totalGB} GB`);
    } catch (e) {
      console.log('Total Capacity: Unable to retrieve');
    }
    
    try {
      const { stdout: availableDisk } = await execPromise(`ideviceinfo -u ${deviceId} -k TotalSystemAvailable`);
      const availableGB = (parseInt(availableDisk.trim()) / 1073741824).toFixed(2);
      console.log(`Available: ${availableGB} GB`);
    } catch (e) {
      console.log('Available Space: Unable to retrieve');
    }
  } catch (error) {
    console.error('Error getting storage info:', error.message);
  }
}

async function getNetworkInfo(deviceId) {
  try {
    console.log(`\n=== Network Information ===`);
    
    try {
      const { stdout: wifiAddress } = await execPromise(`ideviceinfo -u ${deviceId} -k WiFiAddress`);
      console.log(`WiFi MAC Address: ${wifiAddress.trim()}`);
    } catch (e) {
      console.log('WiFi MAC Address: Unable to retrieve');
    }
    
    try {
      const { stdout: btAddress } = await execPromise(`ideviceinfo -u ${deviceId} -k BluetoothAddress`);
      console.log(`Bluetooth MAC Address: ${btAddress.trim()}`);
    } catch (e) {
      console.log('Bluetooth MAC Address: Unable to retrieve');
    }
  } catch (error) {
    console.error('Error getting network info:', error.message);
  }
}

async function getHardwareInfo(deviceId) {
  try {
    console.log(`\n=== Hardware Information ===`);
    
    const keys = [
      { key: 'HardwareModel', label: 'Hardware Model' },
      { key: 'CPUArchitecture', label: 'CPU Architecture' },
      { key: 'ModelNumber', label: 'Model Number' },
      { key: 'RegionInfo', label: 'Region Info' },
    ];
    
    for (const { key, label } of keys) {
      try {
        const { stdout } = await execPromise(`ideviceinfo -u ${deviceId} -k ${key}`);
        console.log(`${label}: ${stdout.trim()}`);
      } catch (e) {
        console.log(`${label}: Unable to retrieve`);
      }
    }
  } catch (error) {
    console.error('Error getting hardware info:', error.message);
  }
}

async function runFullDiagnostics(deviceId) {
  console.log(`\n====================================`);
  console.log(`Running Full Diagnostics on ${deviceId}`);
  console.log(`====================================`);
  
  await getDeviceInfo(deviceId);
  await getBatteryInfo(deviceId);
  await getStorageInfo(deviceId);
  await getNetworkInfo(deviceId);
  await getHardwareInfo(deviceId);
  
  console.log(`\n====================================`);
  console.log(`Diagnostics Complete`);
  console.log(`====================================\n`);
}

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
        case 'WiFiAddress':
          info.wifiAddress = value;
          break;
      }
    }
  });
  
  return info;
}

// Main execution
(async () => {
  const devices = await listDevices();
  
  if (devices.length === 0) {
    console.log('\nNo iOS devices connected. Please connect a device and try again.');
    process.exit(1);
  }
  
  // Run diagnostics on the first device or specified device
  const deviceId = process.argv[2] || devices[0];
  await runFullDiagnostics(deviceId);
})();
