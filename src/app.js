const express = require('express');

const authRoutes = require('./auth/auth.routes');
const orderRoutes = require('./orders/order.routes');

const app = express();

// Body parser
// app.use(bodyParser.json())
app.use(express.json());

// Routes
app.use('/auth', authRoutes);
app.use('/orders', orderRoutes);

module.exports = app;
