const db = require('../config/db');
const orderQueue = require('../config/queue');

/**
 * One-time order
 */
exports.createOneTimeOrder = (user_id, schedule_time, callback) => {
  const q = `
    INSERT INTO orders (user_id, schedule_time, status, is_recurring)
    VALUES (?, ?, 'SCHEDULED', 0)
  `;

  db.query(q, [user_id, schedule_time], (err, result) => {
    if (err) return callback(err);

    const order_id = result.insertId;
    const delay = new Date(schedule_time).getTime() - Date.now();

    orderQueue.add(
      { order_id, user_id },
      { delay: Math.max(delay, 0), attempts: 3 }
    ).then(job => {
      db.query(
        'UPDATE orders SET job_id = ? WHERE order_id = ?',
        [job.id, order_id]
      );
    });

    callback(null, order_id);
  });
};

/**
 * Recurring order
 */
exports.createOrder = (data, callback) => {
  const {
    user_id,
    schedule_time,
    is_recurring,
    repeat_interval,
    repeat_unit,
    max_executions
  } = data;

  const q = `
    INSERT INTO orders (
      user_id,
      schedule_time,
      status,
      is_recurring,
      repeat_interval,
      repeat_unit,
      max_executions,
      execution_count
    )
    VALUES (?, ?, 'SCHEDULED', ?, ?, ?, ?, 0)
  `;

  db.query(
    q,
    [
      user_id,
      schedule_time,
      Number(is_recurring),
      repeat_interval,
      repeat_unit,
      max_executions
    ],
    (err, result) => {
      if (err) return callback(err);

      const order_id = result.insertId;
      const delay = new Date(schedule_time).getTime() - Date.now();

      orderQueue.add(
        { order_id, user_id },
        { delay: Math.max(delay, 0), attempts: 3 }
      ).then(job => {
        db.query(
          'UPDATE orders SET job_id = ? WHERE order_id = ?',
          [job.id, order_id]
        );
      });

      callback(null, order_id);
    }
  );
};

/**
 * Get orders
 */
exports.getOrdersByUser = (user_id, callback) => {
  db.query(
    'SELECT * FROM orders WHERE user_id = ? ORDER BY schedule_time',
    [user_id],
    callback
  );
};

/**
 * Update order (FIXED 🔥)
 */
exports.updateOrder = (order_id, updates, callback) => {
  console.log('RAW BODY:', updates);

  db.query(
    'SELECT * FROM orders WHERE order_id = ?',
    [order_id],
    async (err, rows) => {
      if (err) return callback(err);
      if (!rows.length) return callback(new Error('Order not found'));

      const old = rows[0];

      const merged = {
        schedule_time:
          updates.schedule_time ?? old.schedule_time,

        is_recurring:
          updates.is_recurring !== undefined
            ? Number(updates.is_recurring)
            : old.is_recurring,

        repeat_interval:
          updates.repeat_interval ?? old.repeat_interval,

        repeat_unit:
          updates.repeat_unit ?? old.repeat_unit,

        max_executions:
          updates.max_executions !== undefined
            ? Number(updates.max_executions)
            : old.max_executions
      };


      console.log(merged.max_executions, "i am new max executions")

      if (merged.is_recurring === 0) {
          merged.max_executions = null;
          merged.repeat_interval = null;
          merged.repeat_unit = null;
        }

      // remove old job
      if (old.job_id) {
        const job = await orderQueue.getJob(old.job_id);
        if (job) await job.remove();
      }

      db.query(
        `UPDATE orders SET
          schedule_time = ?,
          is_recurring = ?,
          repeat_interval = ?,
          repeat_unit = ?,
          max_executions = ?,
          execution_count = 0,
          status = 'SCHEDULED',
          job_id = NULL
        WHERE order_id = ?`,
        [
          merged.schedule_time,
          merged.is_recurring,
          merged.repeat_interval,
          merged.repeat_unit,
          merged.max_executions,
          order_id
        ],
        err => {
          if (err) return callback(err);

          const delay =
            new Date(merged.schedule_time).getTime() - Date.now();

          orderQueue.add(
            { order_id, user_id: old.user_id },
            { delay: Math.max(delay, 0), attempts: 3 }
          ).then(job => {
            db.query(
              'UPDATE orders SET job_id = ? WHERE order_id = ?',
              [job.id, order_id],
              err => {
                if (err) return callback(err);
                callback(null); // ✅ ONLY HERE
              }
            );
          });
        }
      );
    }
  );
};


/**
 * Delete order
 */
exports.deleteOrder = (order_id, callback) => {
  db.query(
    'SELECT job_id FROM orders WHERE order_id = ?',
    [order_id],
    async (err, rows) => {
      if (err) return callback(err);

      if (rows.length && rows[0].job_id) {
        const job = await orderQueue.getJob(rows[0].job_id);
        if (job) await job.remove();
      }

      db.query(
        'DELETE FROM orders WHERE order_id = ?',
        [order_id],
        callback
      );
    }
  );
};
