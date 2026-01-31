const orderQueue = require('../config/queue');
const db = require('../config/db');
const { log } = require('../utils/logger');

console.log('🔥 Order worker started and listening...');   // ust to check, worker is working

orderQueue.process(async (job) => {
  const { order_id, user_id } = job.data;

  // log(`ORDER_EXECUTED | order_id=${order_id} | execution=${newCount}`);


  // 1️⃣ Fetch latest order
  const [rows] = await db.promise().query(
    'SELECT * FROM orders WHERE order_id = ?',
    [order_id]
  );

  if (!rows.length) return;

  const order = rows[0];
  const newCount = order.execution_count + 1;

  // 2️⃣ Update execution count
  await db.promise().query(
    'UPDATE orders SET execution_count = ? WHERE order_id = ?',
    [newCount, order_id]
  );

 log(`ORDER_EXECUTED | order_id=${order_id} | execution=${newCount}`);


  // 3️⃣ Decide recurrence
  const shouldRepeat =
    Number(order.is_recurring) === 1 &&
    (order.max_executions === null || newCount < order.max_executions);

  if (shouldRepeat) {
    await scheduleNextRun(order);
  } else {
    await db.promise().query(
      'UPDATE orders SET status = ? WHERE order_id = ?',
      ['COMPLETED', order_id]
    );

   log(`ORDER_COMPLETED | order_id=${order_id}`);

  }
});



/**
 * Schedule next run
 */
async function scheduleNextRun(order) {
  let nextTime = new Date(order.schedule_time);

  if (order.repeat_unit === 'MINUTE') {
    nextTime.setMinutes(nextTime.getMinutes() + order.repeat_interval);
  } else if (order.repeat_unit === 'HOUR') {
    nextTime.setHours(nextTime.getHours() + order.repeat_interval);
  } else if (order.repeat_unit === 'DAY') {
    nextTime.setDate(nextTime.getDate() + order.repeat_interval);
  }

  const delay = nextTime.getTime() - Date.now();

  // update DB FIRST
  await db.promise().query(
    'UPDATE orders SET schedule_time = ?, status = ? WHERE order_id = ?',
    [nextTime, 'SCHEDULED', order.order_id]
  );

  // then enqueue
  await orderQueue.add(
    {
      order_id: order.order_id,
      user_id: order.user_id
    },
    {
      delay: Math.max(delay, 0),
      attempts: 3
    }
  );

  // log(`ORDER_CREATED | user_id=${user_id} | order_id=${order_id}`);


  console.log(`🧩 Next execution scheduled at ${nextTime}`);
}
