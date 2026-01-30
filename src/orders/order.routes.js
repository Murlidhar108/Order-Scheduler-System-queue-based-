const express = require('express');
const router = express.Router();
const controller = require('./order.controller');
const auth = require('../middleware/auth.middleware');

// create order
router.post('/', auth, controller.createOrder);

// view order
router.get('/', auth, controller.getOrders);

//update order
router.put('/:order_id', auth, controller.updateOrder);

// delete order
router.delete('/:order_id', auth, controller.deleteOrder);


module.exports = router;
