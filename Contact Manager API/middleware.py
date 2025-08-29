#middleware.py

import time
from fastapi import Request
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def ip_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Get client IP address
    client_ip = request.client.host if request.client else "Unknown"
    
    # Log the request with IP address
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": process_time,
        "client_ip": client_ip,
        "user_agent": request.headers.get("user-agent", "Unknown")
    }
    
    logging.info(f"Request: {log_data}")
    
    # Add IP address to headers for debugging
    response.headers["X-Client-IP"] = client_ip
    response.headers["X-Process-Time"] = str(process_time)
    
    return response