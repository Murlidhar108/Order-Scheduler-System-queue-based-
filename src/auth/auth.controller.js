const db = require("../config/db");
const { v4: uuidv4 } = require("uuid");

exports.login = (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ message: "Email required" });
  }

  const token = `mock-${uuidv4()}`;

  // Step 1: check if user exists
  const selectQuery = "SELECT user_id FROM users WHERE email = ?";

  db.query(selectQuery, [email], (err, rows) => {
    if (err) {
      console.error("SELECT error:", err);
      return res.status(500).json({ message: "DB error" });
    }

    // Step 2A: user exists → update token
    if (rows.length > 0) {
      const updateQuery = "UPDATE users SET token = ? WHERE email = ?";

      db.query(updateQuery, [token, email], (err) => {
        if (err) {
          console.error("UPDATE error:", err);
          return res.status(500).json({ message: "DB error" });
        }

        return res.json({
          message: "Login successful",
          token
        });
      });

    } 
    // Step 2B: new user → insert
    else {
      const insertQuery = "INSERT INTO users (email, token) VALUES (?, ?)";

      db.query(insertQuery, [email, token], (err) => {
        if (err) {
          console.error("INSERT error:", err);
          return res.status(500).json({ message: "DB error" });
        }

        return res.json({
          message: "Login successful",
          token
        });
      });
    }
  });
};
