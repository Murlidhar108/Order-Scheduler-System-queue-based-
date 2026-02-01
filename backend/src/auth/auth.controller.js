const bcrypt = require('bcryptjs');
const db = require('../config/db');
const { generateToken } = require('../utils/jwt');

exports.signup = async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password)
    return res.status(400).json({ error: 'Email & password required' });

  // check existing user
  const [existing] = await db.promise().query(
    'SELECT * FROM users WHERE email = ?',
    [email]
  );

  if (existing.length)
    return res.status(409).json({ error: 'User already exists' });

  const hashedPassword = await bcrypt.hash(password, 10);

  const [result] = await db.promise().query(
    'INSERT INTO users (email, password) VALUES (?, ?)',
    [email, hashedPassword]
  );

  const user = { id: result.insertId, email };

  const token = generateToken(user);

  await db.promise().query(
    'UPDATE users SET token = ? WHERE user_id = ?',
    [token, user.id]
  );

  res.status(201).json({ token });
};


exports.login = async (req, res) => {
  const { email, password } = req.body;

  const [rows] = await db.promise().query(
    'SELECT * FROM users WHERE email = ?',
    [email]
  );

  if (!rows.length)
    return res.status(401).json({ error: 'Invalid credentials' });

  const user = rows[0];

  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch)
    return res.status(401).json({ error: 'Invalid credentials' });

  const token = generateToken(user);

  await db.promise().query(
    'UPDATE users SET token = ? WHERE user_id = ?',
    [token, user.id]
  );

  res.json({ token });
};

exports.getCurrentUser = async (req, res) => {
  try {
    // req.user is attached by auth.middleware
    res.json({
      id: req.user.id,
      email: req.user.email
    });
  } catch (err) {
    res.status(500).json({
      error: 'Failed to fetch user'
    });
  }
};


exports.logout = async (req, res) => {
  try {
    const userId = req.user.user_id;

    // optional: clear token from DB
    await db.promise().query(
      'UPDATE users SET token = NULL WHERE user_id = ?',
      [userId]
    );

    return res.json({
      message: 'Logged out successfully'
    });
  } catch (err) {
    console.error('Logout error:', err);
    return res.status(500).json({
      error: 'Logout failed'
    });
  }
};
