#main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import create_db_and_tables
from middleware import request_counter_middleware
from routers import notes, auth

app = FastAPI(title="Notes API", version="1.0.0")

# CORS middleware - allow multiple origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:5500",  # Live server or other local server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request counter middleware
app.middleware("http")(request_counter_middleware)

# Include routers
app.include_router(auth.router)
app.include_router(notes.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Notes API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/stats")
async def get_stats():
    from middleware import request_counter
    return {
        "total_requests": request_counter,
        "message": "Check headers for request count and process time"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)