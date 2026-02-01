require('./workers/order.workers');
const cors = require('cors')
const express = require('express');
const path = require('path');


const authRoutes = require('./auth/auth.routes');
const orderRoutes = require('./orders/order.routes');

const app = express();

app.use(cors({
  origin: 'http://localhost:8080', // frontend URL
  credentials: true               // needed if using cookies/JWT in cookies
}));

// Body parser
// app.use(bodyParser.json())
app.use(express.json());
// app.use(express.static(path.join(__dirname, '../public')));    // -----

// Routes
app.use('/auth', authRoutes);
app.use('/orders', orderRoutes);

module.exports = app;
