require('./workers/order.workers');
const express = require('express');
const path = require('path');


const authRoutes = require('./auth/auth.routes');
const orderRoutes = require('./orders/order.routes');

const app = express();

// Body parser
// app.use(bodyParser.json())
app.use(express.json());
// app.use(express.static(path.join(__dirname, '../public')));    // -----

// Routes
app.use('/auth', authRoutes);
app.use('/orders', orderRoutes);

module.exports = app;
