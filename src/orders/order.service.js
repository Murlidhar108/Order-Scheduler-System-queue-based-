const db = require('../config/db');
const orderQueue = require('../config/queue');

exports.createOneTimeOrder = (user_id, schedule_time, callback) => {
  const insert_query = `
    INSERT INTO orders (user_id, schedule_time, status)
    VALUES (?, ?, 'SCHEDULED')
  `;

  db.query(insert_query, [user_id, schedule_time], (err, result) => {
    if (err) return callback(err);

    // MySQL insert id
    const order_id = result.insertId;

    // Calculate delay
    const delay =
      new Date(schedule_time).getTime() - Date.now();

    // Add job to Bull queue
    orderQueue.add(
      {
        order_id,
        user_id
      },
      {
        delay: Math.max(delay, 0),
        attempts: 3
      }
    ).then(job => {
      db.query(
        'UPDATE orders SET job_id = ? WHERE order_id = ?',
        [job.id, order_id]
      )
    })

    callback(null, order_id);
  });
};

// Get all orders for a user
exports.getOrdersByUser = (user_id, callback) => {
  db.query(
    'SELECT * FROM orders WHERE user_id = ? ORDER BY schedule_time ASC',
    [user_id],
    (err, rows) => {
      if (err) return callback(err);
      callback(null, rows);
    }
  );
};


// Update an order
exports.updateOrder = (order_id, updates, callback) => {
  const { schedule_time, status } = updates;

  // 1️⃣ Get old job_id
  db.query(
    'SELECT job_id, user_id FROM orders WHERE order_id = ?',
    [order_id],
    async (err, rows) => {
      if (err) return callback(err);
      if (!rows.length) return callback(new Error('Order not found'));

      const { job_id, user_id } = rows[0];

      // 2️⃣ Remove old job
      if (job_id) {
        const oldJob = await orderQueue.getJob(job_id);
        if (oldJob) await oldJob.remove();
      }

      // 3️⃣ Update DB
      db.query(
        'UPDATE orders SET schedule_time = ?, status = ? WHERE order_id = ?',
        [schedule_time, status, order_id],
        async (err) => {
          if (err) return callback(err);

          // 4️⃣ Add new job
          const delay =
            new Date(schedule_time).getTime() - Date.now();

          const newJob = await orderQueue.add(
            { order_id, user_id },
            { delay: Math.max(delay, 0), attempts: 3 }
          );

          // 5️⃣ Save new job_id
          db.query(
            'UPDATE orders SET job_id = ? WHERE order_id = ?',
            [newJob.id, order_id]
          );

          callback(null);
        }
      );
    }
  );
};

// delete order
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
        (err) => {
          if (err) return callback(err);
          callback(null);
        }
      );
    }
  );
};
