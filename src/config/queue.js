const Queue = require('bull');
const redisConfig = require('./redis');

const orderQueue = new Queue('order-queue', {
  redis: redisConfig
});

module.exports = orderQueue;
