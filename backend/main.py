"""
AyurScan — Backend Deployment Entrypoint.
Enables running directly via:
    uvicorn main:app --host 0.0.0.0 --port $PORT
as well as:
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
"""

import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=False)
