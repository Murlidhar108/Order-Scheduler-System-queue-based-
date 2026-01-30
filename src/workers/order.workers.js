const orderQueue = require('../config/queue');
const db = require('../config/db');

orderQueue.process((job, done) => {
  const { order_id, user_id } = job.data;

  console.log(`🕒 Executing order ${order_id} for user ${user_id}`);

  // simulate order execution
  setTimeout(() => {
    db.query(
      'UPDATE orders SET status = ? WHERE order_id = ?',
      ['COMPLETED', order_id],
      (err) => {
        if (err) return done(err);

        console.log(`✅ Order ${order_id} completed`);
        done();
      }
    );
  }, 1000);
});
