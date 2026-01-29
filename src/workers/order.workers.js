const orderQueue = require('../config/queue');
const db = require('../config/db');

orderQueue.process(async (job) => {
  const { orderId, userId } = job.data;

  console.log(`Placing order ${orderId} for user ${userId}`);

  // Simulate order placement
  await new Promise(r => setTimeout(r, 1000));

  await db.query(
    'UPDATE orders SET status = ? WHERE id = ?',
    ['COMPLETED', orderId]
  );

  console.log(`Order ${orderId} completed`);
});
