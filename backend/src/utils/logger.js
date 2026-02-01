const fs = require('fs');
const path = require('path');

// ✅ Use existing logs folder
const logFile = path.join(__dirname, '../logs/orders.log');

function getISTTime() {
  const now = new Date();
  return now.toLocaleString('en-IN', {
    timeZone: 'Asia/Kolkata',
    hour12: false
  });
}

/**
 * Robust logging function
 */
function log(message) {
  try {
    const line = `[${getISTTime()}] ${message}\n`;

    // Append synchronously to avoid race conditions
    fs.appendFileSync(logFile, line, 'utf8');
  } catch (err) {
    // Fallback: print to console if file write fails
    console.error('⚠️ Logger failed:', err.message);
    console.log(`[${getISTTime()}] ${message}`);
  }
}

module.exports = { log };
