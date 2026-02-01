# Order Scheduler UI

A simple Python GUI application for scheduling one-time and recurring orders.

## Features

### 1. Authentication
- **Sign Up**: Create a new account with email and password
- **Login**: Access your account
- **Logout**: Securely log out

### 2. Order Management
- **Create Orders**: Schedule one-time or recurring orders
  - One-time orders: Set a specific execution time
  - Recurring orders: Configure repeat interval, unit (MINUTE/HOUR/DAY/WEEK/MONTH), and max executions
- **View Orders**: See all your orders with status and details
- **Update Orders**: Modify existing orders
- **Delete Orders**: Remove orders you no longer need

## Installation

1. **Install Python** (3.7 or higher)

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start your backend server** on `http://localhost:3000`

2. **Run the application**:
   ```bash
   python order_scheduler_ui.py
   ```

3. **Sign Up or Login**:
   - Enter your email and password
   - Click "Sign Up" to create a new account or "Login" to access existing account

4. **Create an Order**:
   - Enter schedule time in format: `YYYY-MM-DD HH:MM:SS` (e.g., `2026-02-03 14:30:00`)
   - For one-time orders: Leave "Recurring Order" unchecked
   - For recurring orders:
     - Check "Recurring Order"
     - Set repeat interval (number)
     - Select repeat unit (MINUTE, HOUR, DAY, WEEK, MONTH)
     - Set max executions
   - Click "Create Order"

5. **View Your Orders**:
   - Orders are displayed in the right panel
   - Legend: `R` = Recurring, `O` = One-time
   - Click "🔄 Refresh" to reload the list

6. **Manage Orders**:
   - Select an order from the list
   - Click "View Details" to see full order information
   - Click "Update" to modify the order
   - Click "Delete" to remove the order

## Date Format

All dates should be in the format: `YYYY-MM-DD HH:MM:SS`

Examples:
- `2026-02-03 14:30:00`
- `2026-12-25 09:00:00`
- `2026-03-15 18:45:30`

## Repeat Units

- **MINUTE**: Order repeats every X minutes
- **HOUR**: Order repeats every X hours
- **DAY**: Order repeats every X days
- **WEEK**: Order repeats every X weeks
- **MONTH**: Order repeats every X months

## Troubleshooting

### Connection Error
- Ensure your backend server is running on `http://localhost:3000`
- Check your internet/network connection
- Verify the backend APIs are accessible

### Login/Signup Failed
- Check your credentials
- Ensure the backend authentication service is running
- Verify the API endpoints are correct

### Orders Not Loading
- Try clicking the "🔄 Refresh" button
- Check if you're properly logged in (token is valid)
- Verify the backend orders service is running

## API Endpoints Used

- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Authenticate user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user details
- `POST /orders/create` - Create new order
- `GET /orders/` - Get all user orders
- `PUT /orders/:order_id` - Update specific order
- `DELETE /orders/:order_id` - Delete specific order

## Notes

- All API calls include JWT token in Authorization header (except signup/login)
- Dates are converted to ISO format before sending to backend
- The application stores the JWT token in memory (not persisted)