# E-Commerce API

A modular FastAPI e-commerce application with cart and checkout system.

```
ecommerce_api/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── products.py
│   ├── cart.py
│   ├── users.py
│   └── admin.py
├── models.py
├── database.py
├── auth.py
├── middleware.py
├── orders.json
├── requirements.txt
└── README.md



## Features

- **User Authentication**: JWT-based authentication system
- **Product Management**: CRUD operations for products (admin only)
- **Shopping Cart**: Add, remove, and view cart items
- **Checkout System**: Process orders and update inventory
- **Order Management**: Save orders to JSON file for backup
- **Response Time Middleware**: Measure and add response time to headers

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
Run the application:

bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
API Endpoints
Authentication
POST /auth/register - Register new user

POST /auth/login - Login to get JWT token

Products (Public)
GET /products/ - Get all products

GET /products/{id} - Get specific product

Products (Admin Only)
POST /products/ - Create new product

PUT /products/{id} - Update product

DELETE /products/{id} - Delete product

Cart
GET /cart/ - Get user's cart

POST /cart/add - Add item to cart

POST /cart/checkout - Checkout and create order

DELETE /cart/item/{id} - Remove item from cart

DELETE /cart/clear - Clear entire cart

Usage
Register a user:

bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
Login to get token:

bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=password123"
Add product to cart (using the token):

bash
curl -X POST "http://localhost:8000/cart/add?product_id=1&quantity=2" \
  -H "Authorization: Bearer YOUR_TOKEN"
Checkout:

bash
curl -X POST "http://localhost:8000/cart/checkout" \
  -H "Authorization: Bearer YOUR_TOKEN"
Admin Features
To create an admin user, register with is_admin: true:

json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin123",
  "is_admin": true
}
Order Backup
All orders are saved to orders.json for backup purposes.

Response Time
The API includes response time measurement in the X-Process-Time header.

text

## Usage Examples

### 1. Create Admin User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "email": "admin@example.com", "password": "admin123", "is_admin": true}'
2. Create Product (Admin)
bash
curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "stock": 10, "description": "Gaming laptop"}'
3. Add to Cart
bash
curl -X POST "http://localhost:8000/cart/add?product_id=1&quantity=1" \
  -H "Authorization: Bearer USER_TOKEN"
4. Checkout
bash
curl -X POST "http://localhost:8000/cart/checkout" \
  -H "Authorization: Bearer USER_TOKEN"