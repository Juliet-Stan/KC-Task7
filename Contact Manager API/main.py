#main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import create_db_and_tables
from middleware import ip_logging_middleware
from routers import contacts, auth

app = FastAPI(title="Contact Manager API", version="1.0.0")

# CORS middleware - allow multiple origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IP logging middleware
app.middleware("http")(ip_logging_middleware)

# Include routers
app.include_router(auth.router)
app.include_router(contacts.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Contact Manager API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)