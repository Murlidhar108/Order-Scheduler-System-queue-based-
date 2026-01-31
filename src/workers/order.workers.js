const orderQueue = require('../config/queue');
const db = require('../config/db');

console.log('🔥 Order worker started and listening...');   // ust to check, worker is working

orderQueue.process(async (job) => {     // bull calls jon when active
  const { order_id, user_id } = job.data;

  console.log(`🕒 Executing order ${order_id} for user ${user_id}`);

  // 1️⃣ Fetch order  (latest db details)
  const [rows] = await db.promise().query(
    'SELECT * FROM orders WHERE order_id = ?',
    [order_id]
  );

  if (!rows.length) {
    console.log('⚠️ Order not found:', order_id);
    return;
  }

  const order = rows[0];
  const newCount = order.execution_count + 1;  // new count

  // 2️⃣ Update execution count
  await db.promise().query(
    'UPDATE orders SET execution_count = ? WHERE order_id = ?',
    [newCount, order_id]
  );

  console.log(`✅ execution_count updated → ${newCount}`);

  // 3️⃣ Recurring logic
  if (
    Number(order.is_recurring) === 1 &&
    (order.max_executions === null || newCount < order.max_executions)
  ) {
    console.log('🔁 Scheduling next execution');
    // await scheduleNextRun(order);
    db.query(
  'SELECT * FROM orders WHERE order_id = ?',
  [order_id],
  (err, freshRows) => {
    if (err || !freshRows.length) return;

    const freshOrder = freshRows[0];

    if (
      Number(freshOrder.is_recurring) === 1 &&
      (freshOrder.max_executions === null||    // changed this from !freshOrder.max_executions
        newCount < freshOrder.max_executions)
    ) {
      scheduleNextRun(freshOrder);
    } else {
      db.query(
        'UPDATE orders SET status = ? WHERE order_id = ?',
        ['COMPLETED', order_id]
      );
      console.log(`🏁 Order ${order_id} completed`);
    }
  }
);

  } else {
    await db.promise().query(
      'UPDATE orders SET status = ? WHERE order_id = ?',
      ['COMPLETED', order_id]
    );
    console.log(`🏁 Order ${order_id} completed`);
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

  console.log(`🧩 Next execution scheduled at ${nextTime}`);
}
