#readme.md

Job Application Tracker API
A comprehensive FastAPI backend application for tracking job applications with authentication, search functionality, and proper authorization.

Features
User Authentication: JWT-based authentication system

Job Application Management: Full CRUD operations for job applications

Search Functionality: Filter applications by status and company

Authorization: Users can only access their own applications

Input Validation: Comprehensive validation for all inputs

Error Handling: Proper error responses with HTTP status codes

Security: Password hashing with bcrypt

Middleware: User-Agent header validation

Tech Stack
Backend: FastAPI

Database: SQLite with SQLModel

Authentication: JWT tokens

Password Hashing: bcrypt

Validation: Pydantic models

Project Structure

```
job_application_tracker/
├── main.py              # FastAPI application and middleware
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── database.py          # Database configuration
├── auth.py             # Authentication utilities
├── dependencies.py     # Dependency injection
├── routers/
│   ├── __init__.py
│   ├── applications.py  # Job application endpoints
│   └── auth.py         # Authentication endpoints
├── requirements.txt     # Dependencies
├── job_applications.db # SQLite database (auto-generated)
└── README.md


```
Installation
Install dependencies:


```bash
pip install -r requirements.txt
Run the application:


```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
API Endpoints
Authentication Endpoints
POST /auth/register - Register a new user

POST /auth/login - Login to get JWT token

Application Endpoints (Require Authentication)
POST /applications/ - Create a new job application

GET /applications/ - Get all user's applications

GET /applications/{id} - Get specific application

GET /applications/search/ - Search applications by status/company

PUT /applications/{id} - Update an application

DELETE /applications/{id} - Delete an application

Usage Examples
1. Register a New User

bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MyJobTracker/1.0" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
2. Login to Get Token
bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: MyJobTracker/1.0" \
  -d "username=john_doe&password=securepassword123"
Response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
3. Create a Job Application
bash
curl -X POST "http://localhost:8000/applications/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MyJobTracker/1.0" \
  -d '{
    "company": "Google",
    "position": "Senior Software Engineer",
    "status": "interview",
    "date_applied": "2024-01-15T10:00:00",
    "notes": "Technical interview scheduled for next week"
  }'
4. Get All Applications
bash
curl -X GET "http://localhost:8000/applications/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "User-Agent: MyJobTracker/1.0"
5. Search Applications by Status
bash
curl -X GET "http://localhost:8000/applications/search/?status=interview" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "User-Agent: MyJobTracker/1.0"
6. Search Applications by Company
bash
curl -X GET "http://localhost:8000/applications/search/?company=google" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "User-Agent: MyJobTracker/1.0"
7. Update an Application
bash
curl -X PUT "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MyJobTracker/1.0" \
  -d '{
    "status": "offered",
    "notes": "Received offer letter, negotiating salary"
  }'
8. Delete an Application
bash
curl -X DELETE "http://localhost:8000/applications/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "User-Agent: MyJobTracker/1.0"
Application Status Values
The API accepts the following status values:

pending - Application submitted, waiting for response

interview - Interview scheduled or in progress

rejected - Application rejected

offered - Job offer received

accepted - Offer accepted

Error Responses
Missing User-Agent Header
json
{
  "detail": "Missing User-Agent header"
}
Invalid Credentials
json
{
  "detail": "Incorrect username or password"
}
Invalid Status
json
{
  "detail": "Status must be one of: pending, interview, rejected, offered, accepted"
}
Unauthorized Access
json
{
  "detail": "Not authorized to access this application"
}
Application Model
json
{
  "id": 1,
  "company": "Google",
  "position": "Senior Software Engineer",
  "status": "interview",
  "date_applied": "2024-01-15T10:00:00",
  "notes": "Technical interview scheduled",
  "user_id": 1,
  "created_at": "2024-01-15T10:05:00.000Z",
  "updated_at": "2024-01-15T10:05:00.000Z"
}
Authentication Flow
User registers with username, email, and password

Password is hashed and stored securely

User logs in with username and password

Server returns JWT token

Token is included in Authorization header for protected endpoints

Token expires after 30 minutes

Security Features
Password hashing with bcrypt

JWT token authentication

Input validation with Pydantic

User authorization (users can only access their own data)

SQL injection prevention through ORM

User-Agent header validation

Development
Running in Development Mode
bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Accessing API Documentation
Once running, access the interactive API documentation:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Testing the API
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

Database errors: The database is automatically created on first run

Authentication errors: Ensure the token is included in the Authorization header

User-Agent errors: All requests must include a User-Agent header

Testing Authentication
First register a user

Login to get a token

Use the token in the Authorization header for all protected endpoints

License
This project is for educational purposes. Feel free to modify and use as needed.

Support
For issues or questions, please ensure:

All dependencies are properly installed

The User-Agent header is included in all requests

Valid JWT tokens are used for authenticated endpoints

The API will return appropriate error messages with details on how to fix the issue.