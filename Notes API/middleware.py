#middleware.py

import time
from fastapi import Request
import logging
from datetime import datetime

# Global request counter
request_counter = 0

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def request_counter_middleware(request: Request, call_next):
    global request_counter
    request_counter += 1
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log the request
    log_data = {
        "request_number": request_counter,
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": process_time,
        "client_host": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent", "Unknown")
    }
    
    logging.info(f"Request #{request_counter}: {log_data}")
    
    # Add request count to headers
    response.headers["X-Total-Requests"] = str(request_counter)
    response.headers["X-Process-Time"] = str(process_time)
    
    return response