const express = require('express');
const router = express.Router();
const controller = require('./order.controller');
const auth = require('../middleware/auth.middleware');

router.post('/', auth, controller.createOrder);

module.exports = router;
