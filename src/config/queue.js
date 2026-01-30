const Queue = require('bull');

const orderQueue = new Queue('order-queue', {
  redis: {
    host: '127.0.0.1',
    port: 6379
  }
});

orderQueue.on('error', (err) => {
  console.error('Bull queue error:', err);
});

module.exports = orderQueue;
