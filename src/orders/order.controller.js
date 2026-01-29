const service = require('./order.service');

exports.createOrder = (req, res) => {
  const { schedule_time } = req.body;
  const user_id = req.user.user_id;

  service.createOneTimeOrder(user_id, schedule_time, (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to schedule order' });
    }

    res.json({ message: 'Order scheduled successfully' });
  });
};
