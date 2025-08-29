#readme.md

# Notes API

A comprehensive FastAPI backend application for managing notes with authentication, file backup, and request tracking.

Project Structure
```
notes_api/
├── main.py
├── models.py
├── database.py
├── auth.py
├── middleware.py
├── routers/
│   ├── __init__.py
│   └── notes.py
├── notes.json
├── requirements.txt
└── README.md

```

## Features

- **User Authentication**: JWT-based authentication system
- **Note Management**: Full CRUD operations for notes
- **File Backup**: Automatic backup of all notes to JSON file
- **Request Tracking**: Middleware to count and log all requests
- **CORS Support**: Multiple origins allowed
- **Authorization**: Users can only access their own notes

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login to get JWT token (form data)
- `GET /auth/me` - Get current user info

### Notes (Require Authentication)
- `POST /notes/` - Create new note
- `GET /notes/` - Get all user's notes
- `GET /notes/{id}` - Get specific note
- `PUT /notes/{id}` - Update note
- `DELETE /notes/{id}` - Delete note

### Stats
- `GET /stats` - Get total request count

## Usage Examples

### 1. Register User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
2. Login (Form Data)
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=password123"
3. Create Note
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Note", "content": "This is the content of my note"}'
4. Get All Notes
```bash
curl -X GET "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN"
Middleware Features
Request Counting: Tracks total number of requests made

Request Logging: Logs all requests to app.log

Response Headers: Adds X-Total-Requests and X-Process-Time headers

File Backup
All notes are automatically backed up to notes.json after every create, update, or delete operation.

CORS Origins
The API allows requests from:

http://localhost:3000 (React development server)

http://127.0.0.1:5500 (Live server or other local server)

text

## Usage Examples

### Register a user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
Login (using form data):
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1&password=password123"
Create a note:
```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Shopping List", "content": "Milk, Eggs, Bread"}'
  
Get all notes:
```bash
curl -X GET "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_TOKEN"
This Notes API includes all the requested features: authentication, note management, middleware for request counting and logging, file backup to JSON, and CORS support for multiple origins.