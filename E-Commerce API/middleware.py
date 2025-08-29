#middleware.py

import time
from fastapi import Request
import logging

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def response_time_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Add response time to headers
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log the request
    log_data = {
        "timestamp": time.time(),
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": process_time,
        "client_host": request.client.host if request.client else None
    }
    
    logging.info(f"Request: {log_data}")
    return response