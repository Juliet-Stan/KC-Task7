#readme.md

Student Management System
A comprehensive FastAPI backend application for managing students and their grades with authentication, authorization, and database integration.

Features
Student Management: Full CRUD operations for student records

Authentication & Authorization: JWT-based authentication system

Database Integration: SQLite database with SQLModel ORM

Security: Password hashing with bcrypt

CORS Support: Configured for frontend integration

Request Logging: Middleware to log all requests to a file

Input Validation: Pydantic models for data validation

Error Handling: Comprehensive error handling with proper HTTP status codes

Tech Stack
Backend: FastAPI

Database: SQLite with SQLModel

Authentication: JWT tokens

Password Hashing: bcrypt

Logging: Python logging module

Project Structure
text
student_management_system/
├── main.py              # FastAPI application and endpoints
├── models.py            # Database and Pydantic models
├── database.py          # Database configuration
├── auth.py             # Authentication utilities
├── requirements.txt     # Dependencies
├── students.db         # SQLite database (auto-generated)
├── users.json          # User storage (auto-generated)
└── app.log            # Request logs (auto-generated)
Installation
Clone the repository or create the project files

Install dependencies:

bash
pip install -r requirements.txt
Run the application:

bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
API Endpoints
Authentication Endpoints
POST /token - Login to get JWT token

POST /register - Register a new user

Student Endpoints (Require Authentication)
GET /students/ - Get all students

GET /students/{id} - Get specific student

POST /students/ - Create new student

PUT /students/{id} - Update student

DELETE /students/{id} - Delete student

Public Endpoints
GET / - API information

GET /health - Health check

Default Credentials
The system creates a default admin user on startup:

Username: admin

Password: admin123

Usage Examples
1. Register a New User
bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123&email=admin@school.com"
2. Login to Get Token
bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
Response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
3. Create a Student
bash
curl -X POST "http://localhost:8000/students/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "age": 20,
       "email": "john@example.com",
       "grades": ["A", "B", "A"]
     }'
4. Get All Students
bash
curl -X GET "http://localhost:8000/students/" \
     -H "Authorization: Bearer YOUR_TOKEN"
5. Update a Student
bash
curl -X PUT "http://localhost:8000/students/1" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Smith",
       "grades": ["A", "A", "B"]
     }'
6. Delete a Student
bash
curl -X DELETE "http://localhost:8000/students/1" \
     -H "Authorization: Bearer YOUR_TOKEN"
Student Model
python
{
  "id": 1,
  "name": "John Doe",
  "age": 20,
  "email": "john@example.com",
  "grades": ["A", "B", "A"],
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
Authentication Flow
User registers or uses default credentials

User logs in to receive JWT token

Token is included in Authorization header for protected endpoints

Token expires after 30 minutes (configurable)

Database Schema
The application uses SQLite with the following table structure:

sql
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    grades VARCHAR NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
Logging
All requests are logged to app.log with the following format:

text
2024-01-15 10:30:00,000 - INFO - Request: {
  "timestamp": "2024-01-15T10:30:00.000Z",
  "method": "GET",
  "url": "http://localhost:8000/students/",
  "status_code": 200,
  "process_time": 0.002,
  "client_host": "127.0.0.1"
}
CORS Configuration
The API is configured to allow requests from:

http://localhost:3000 (React/Vue/Angular development server)

Error Handling
The API returns appropriate HTTP status codes:

200 - Success

201 - Created

400 - Bad Request

401 - Unauthorized

404 - Not Found

500 - Internal Server Error

Security Features
Password hashing with bcrypt

JWT token authentication

Input validation with Pydantic

SQL injection prevention through ORM

CORS configuration

Request logging

Development
Running in Development Mode
bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Accessing API Documentation
Once running, access the interactive API documentation:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Testing
You can test the API using:

curl commands (as shown above)

Postman

Thunder Client (VS Code extension)

The interactive Swagger documentation

Production Considerations
For production deployment, consider:

Changing the SECRET_KEY in auth.py

Using a production-grade database (PostgreSQL, MySQL)

Setting up proper SSL/TLS certificates

Implementing rate limiting

Adding more comprehensive logging

Setting up monitoring and alerting

Using environment variables for configuration

Troubleshooting
Common Issues
Port already in use: Change the port with --port 8001

Database errors: Delete students.db to reset the database

Authentication errors: Check that the token is included in the Authorization header

Logs
Check app.log for detailed request information and errors.

License
This project is for educational purposes. Feel free to modify and use as needed.

Support
For issues or questions, please check the logs and ensure all dependencies are properly installed.