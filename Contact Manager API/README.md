#readme.md

# Contact Manager API

A comprehensive FastAPI backend application for managing contacts with authentication, authorization, and IP logging.

Project Structure
```
contact_manager/
├── main.py
├── models.py
├── database.py
├── auth.py
├── middleware.py
├── routers/
│   ├── __init__.py
│   ├── contacts.py
│   └── auth.py
├── requirements.txt
└── README.md
```

## Features

- **User Authentication**: JWT-based authentication system
- **Contact Management**: Full CRUD operations for contacts
- **Search Functionality**: Search contacts by name, email, phone, or address
- **Authorization**: Users can only access their own contacts
- **IP Logging**: Middleware to log IP address of every request
- **CORS Support**: Multiple origins allowed
- **Input Validation**: Comprehensive validation for all inputs

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login to get JWT token (form data)
- `GET /auth/me` - Get current user info

### Contacts (Require Authentication)
- `POST /contacts/` - Create new contact
- `GET /contacts/` - Get all user's contacts
- `GET /contacts/{id}` - Get specific contact
- `PUT /contacts/{id}` - Update contact
- `DELETE /contacts/{id}` - Delete contact
- `GET /contacts/search/` - Search contacts

## Usage Examples

### 1. Register User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
2. Login (Form Data)
bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=password123"
3. Create Contact
bash
curl -X POST "http://localhost:8000/contacts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "phone": "+1234567890", "address": "123 Main St"}'
4. Get All Contacts
bash
curl -X GET "http://localhost:8000/contacts/" \
  -H "Authorization: Bearer YOUR_TOKEN"
5. Search Contacts
bash
curl -X GET "http://localhost:8000/contacts/search/?q=john" \
  -H "Authorization: Bearer YOUR_TOKEN"
Middleware Features
IP Logging: Logs client IP address for every request

Request Logging: Logs all requests to app.log with detailed information

Response Headers: Adds X-Client-IP and X-Process-Time headers

CORS Origins
The API allows requests from:

http://localhost:3000

http://127.0.0.1:3000

http://localhost:8000

http://127.0.0.1:8000

Security Features
Password hashing with bcrypt

JWT token authentication

Input validation with Pydantic

User authorization (users can only access their own data)

SQL injection prevention through ORM

IP address logging for security monitoring


## Installation & Running

1. Install dependencies:
```bash
pip install -r requirements.txt
Run the application:

bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Testing the API
Register a user:
bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
Login:
bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=password123"
Create a contact:
bash
curl -X POST "http://localhost:8000/contacts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "email": "alice@example.com", "phone": "+1234567890"}'
Get all contacts:
bash
curl -X GET "http://localhost:8000/contacts/" \
  -H "Authorization: Bearer YOUR_TOKEN"
This Contact Manager API includes all the requested features: JWT authentication, contact CRUD operations, dependency injection for database, IP logging middleware, and CORS support.