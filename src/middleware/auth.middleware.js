const jwt = require('jsonwebtoken');
const db = require('../config/db');

module.exports = async (req, res, next) => {
  try {
    // 1️⃣ Get token from header
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).json({
        error: 'No token provided'
      });
    }

    const token = authHeader.split(' ')[1]; // Bearer <token>

    console.log('Auth Header:', req.headers.authorization);


    // 2️⃣ Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

console.log('Decoded token:', decoded);
console.log('decoded id:', decoded.user_id)

const [rows] = await db.promise().query(
  'SELECT * FROM users WHERE user_id = ?',
  [decoded.user_id]
);

if (!rows.length) {
  return res.status(401).json({
    error: 'Session expired, please login again'
  });
}

req.user = rows[0];
next();


  } catch (err) {
    // ✅ THIS IS WHERE YOUR CODE GOES
    return res.status(401).json({
      error: 'Session expired, please login again'
    });
  }
};
