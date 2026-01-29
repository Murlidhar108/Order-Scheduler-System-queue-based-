const db = require('../config/db');

exports.createOneTimeOrder = (user_id, schedule_time, callback) => {
  const query = `
    INSERT INTO orders (user_id, schedule_time, status)
    VALUES (?, ?, 'SCHEDULED')
  `;

  db.query(query, [user_id, schedule_time], callback);
};
