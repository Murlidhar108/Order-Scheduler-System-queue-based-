const fs = require('fs');
const path = require('path');

// ✅ use existing logs folder
const logFile = path.join(__dirname, '../logs/orders.log');

function getISTTime() {
  const now = new Date();
  return now.toLocaleString('en-IN', {
    timeZone: 'Asia/Kolkata',
    hour12: false
  });
}

function log(message) {
try {
     const line = `[${getISTTime()}] ${message}\n`;
     fs.appendFileSync(logFile, line, 'utf8');
} catch(err) {
     console.error('⚠️ Logger failed:', err.message);
}
}

module.exports = { log };
