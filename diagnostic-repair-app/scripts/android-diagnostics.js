#!/usr/bin/env node

/**
 * Android Diagnostic Script
 * Uses ADB to run diagnostics on connected Android devices
 */

const adb = require('adbkit');
const client = adb.createClient();

async function listDevices() {
  try {
    const devices = await client.listDevices();
    console.log('Connected Android devices:');
    devices.forEach((device, index) => {
      console.log(`${index + 1}. ${device.id} (${device.type})`);
    });
    return devices;
  } catch (error) {
    console.error('Error listing devices:', error.message);
    return [];
  }
}

async function getDeviceInfo(deviceId) {
  try {
    console.log(`\n=== Device Information ===`);
    const properties = await client.getProperties(deviceId);
    
    console.log(`Manufacturer: ${properties['ro.product.manufacturer']}`);
    console.log(`Model: ${properties['ro.product.model']}`);
    console.log(`Brand: ${properties['ro.product.brand']}`);
    console.log(`Android Version: ${properties['ro.build.version.release']}`);
    console.log(`SDK Version: ${properties['ro.build.version.sdk']}`);
    console.log(`Serial Number: ${properties['ro.serialno']}`);
    console.log(`Build ID: ${properties['ro.build.id']}`);
    
    return properties;
  } catch (error) {
    console.error('Error getting device info:', error.message);
  }
}

async function getBatteryInfo(deviceId) {
  try {
    console.log(`\n=== Battery Information ===`);
    const output = await client.shell(deviceId, 'dumpsys battery');
    const data = await streamToString(output);
    
    const lines = data.split('\n');
    lines.forEach(line => {
      if (line.includes('level:') || 
          line.includes('health:') || 
          line.includes('status:') || 
          line.includes('temperature:') || 
          line.includes('voltage:')) {
        console.log(line.trim());
      }
    });
  } catch (error) {
    console.error('Error getting battery info:', error.message);
  }
}

async function getStorageInfo(deviceId) {
  try {
    console.log(`\n=== Storage Information ===`);
    const output = await client.shell(deviceId, 'df -h');
    const data = await streamToString(output);
    console.log(data);
  } catch (error) {
    console.error('Error getting storage info:', error.message);
  }
}

async function getMemoryInfo(deviceId) {
  try {
    console.log(`\n=== Memory Information ===`);
    const output = await client.shell(deviceId, 'cat /proc/meminfo | head -10');
    const data = await streamToString(output);
    console.log(data);
  } catch (error) {
    console.error('Error getting memory info:', error.message);
  }
}

async function getCPUInfo(deviceId) {
  try {
    console.log(`\n=== CPU Information ===`);
    const output = await client.shell(deviceId, 'cat /proc/cpuinfo | grep -E "processor|model name|cpu MHz"');
    const data = await streamToString(output);
    console.log(data);
  } catch (error) {
    console.error('Error getting CPU info:', error.message);
  }
}

async function getNetworkInfo(deviceId) {
  try {
    console.log(`\n=== Network Information ===`);
    const output = await client.shell(deviceId, 'ip addr show');
    const data = await streamToString(output);
    console.log(data);
  } catch (error) {
    console.error('Error getting network info:', error.message);
  }
}

async function runFullDiagnostics(deviceId) {
  console.log(`\n====================================`);
  console.log(`Running Full Diagnostics on ${deviceId}`);
  console.log(`====================================`);
  
  await getDeviceInfo(deviceId);
  await getBatteryInfo(deviceId);
  await getStorageInfo(deviceId);
  await getMemoryInfo(deviceId);
  await getCPUInfo(deviceId);
  await getNetworkInfo(deviceId);
  
  console.log(`\n====================================`);
  console.log(`Diagnostics Complete`);
  console.log(`====================================\n`);
}

function streamToString(stream) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    stream.on('data', chunk => chunks.push(chunk));
    stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    stream.on('error', reject);
  });
}

// Main execution
(async () => {
  const devices = await listDevices();
  
  if (devices.length === 0) {
    console.log('No Android devices connected. Please connect a device and try again.');
    process.exit(1);
  }
  
  // Run diagnostics on the first device
  const deviceId = process.argv[2] || devices[0].id;
  await runFullDiagnostics(deviceId);
})();
