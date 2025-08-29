main.py

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import create_db_and_tables
from routers import applications, auth

app = FastAPI(title="Job Application Tracker", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User-Agent middleware
@app.middleware("http")
async def reject_missing_user_agent(request: Request, call_next):
    if "User-Agent" not in request.headers:
        return Response(
            status_code=400,
            content="Missing User-Agent header"
        )
    response = await call_next(request)
    return response

# Include routers
app.include_router(auth.router)
app.include_router(applications.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Job Application Tracker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)