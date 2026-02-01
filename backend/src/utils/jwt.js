const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'supersecretkey';

function generateToken(user) {
  return jwt.sign(
  { user_id: user.user_id }, // 🔥 MUST be ID
  process.env.JWT_SECRET,
  { expiresIn: '1d' }
);

}

function verifyToken(token) {
  return jwt.verify(token, JWT_SECRET);
}

module.exports = { generateToken, verifyToken };
