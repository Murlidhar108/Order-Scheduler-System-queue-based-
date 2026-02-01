const service = require('./order.service');

exports.createOrder = (req, res) => {

  console.log("i am working")
  
  const {
    schedule_time,
    is_recurring = false,
    repeat_interval = null,
    repeat_unit = null,
    max_executions = null
  } = req.body;

  const user_id = req.user.user_id;

  console.log("i am working")

  service.createOrder(
    {
      user_id,
      schedule_time,
      is_recurring,
      repeat_interval,
      repeat_unit,
      max_executions
    },
    (err, order_id) => {
      if (err) {
        console.error(err);
        return res.status(500).json({ error: 'Failed to create order' });
      }

      res.json({
        message: 'Order scheduled successfully',
        order_id
      });
    }
  );
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

  console.log('REQ BODY:', req.body);

  console.log(order_id);
  const { schedule_time, status } = req.body;

  service.updateOrder(order_id, req.body, (err) => {
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


exports.logout = async (req, res) => {
  await db.promise().query(
    'UPDATE users SET token = NULL WHERE id = ?',
    [req.user.id]
  );

  res.json({ message: 'Logged out successfully' });
};