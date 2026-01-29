const db = require('../config/db');

module.exports = (req, res, next) => {
    const authHeader = req.headers['authorization'];

    if (!authHeader) {
        return res.status(401).json({ error: 'Missing Authorization header' });
    }

    // Expecting: Authorization: Bearer <token>
    const token = authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Invalid Authorization format' });
    }

    const query = 'SELECT user_id, email FROM users WHERE token = ?';

    db.query(query, [token], (err, rows) => {
        if (err) {
            console.error('Auth DB error:', err);
            return res.status(500).json({ error: 'Auth middleware error' });
        }

        if (rows.length === 0) {
            return res.status(401).json({ error: 'Invalid token' });
        }

        // Attach user to request
        req.user = {
            user_id: rows[0].user_id,
            email: rows[0].email
        };

        next();
    });
};
