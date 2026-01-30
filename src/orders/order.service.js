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
    );

    callback(null, order_id);
  });
};
