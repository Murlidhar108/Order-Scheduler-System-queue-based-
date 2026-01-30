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

// View all orders for a user
exports.getOrders = (req, res) => {
  const user_id = req.user.user_id;

  service.getOrdersByUser(user_id, (err, orders) => {
    if (err) return res.status(500).json({ error: 'DB error' });

    res.json({ orders });
  });
};

// Update order 
exports.updateOrder = (req, res) => {
  console.log("working");
  const { order_id } = req.params;
  console.log(order_id);
  const { schedule_time, status } = req.body;

  service.updateOrder(order_id, { schedule_time, status }, (err) => {
    if (err) return res.status(500).json({ error: 'DB error' });

    res.json({ message: 'Order updated successfully' });
  });
};

// Delete order
exports.deleteOrder = (req, res) => {
  const { order_id } = req.params;

  console.log('🗑️ Delete order hit:', order_id);

  service.deleteOrder(order_id, (err) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'Failed to delete order' });
    }

    res.json({ message: 'Order deleted successfully' });
  });
};
