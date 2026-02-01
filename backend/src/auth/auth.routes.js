const express = require("express");
const router = express.Router();
const { login, signup, getCurrentUser, logout} = require("./auth.controller");
const authMiddleware = require("../middleware/auth.middleware")

router.post('/signup', signup);
router.post('/login', login);
router.post('/logout', authMiddleware, logout);
router.get('/me', authMiddleware, getCurrentUser);


module.exports = router;
