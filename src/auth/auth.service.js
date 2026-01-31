const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../config/db');

const JWT_SECRET = process.env.JWT_SECRET || 'dev_secret';

exports.signup = async (email, password) => {
  const [rows] = await db.promise().query(
    'SELECT id FROM users WHERE email = ?',
    [email]
  );

  if (rows.length) {
    throw new Error('User already exists');
  }

  const hash = await bcrypt.hash(password, 10);

  const [result] = await db.promise().query(
    'INSERT INTO users (email, password_hash) VALUES (?, ?)',
    [email, hash]
  );

  return jwt.sign(
    { userId: result.insertId, email },
    JWT_SECRET,
    { expiresIn: '1d' }
  );
};

exports.login = async (email, password) => {
  const [rows] = await db.promise().query(
    'SELECT * FROM users WHERE email = ?',
    [email]
  );

  if (!rows.length) {
    throw new Error('Invalid credentials');
  }

  const user = rows[0];
  const match = await bcrypt.compare(password, user.password_hash);

  if (!match) {
    throw new Error('Invalid credentials');
  }

  return jwt.sign(
    { userId: user.id, email },
    JWT_SECRET,
    { expiresIn: '1d' }
  );
};
