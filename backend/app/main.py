"""
AyurScan - AI-Powered Ayurvedic Plant Identification Backend.
FastAPI Main Application.
"""

import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Configure environment before app imports
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / ".env"
if not env_file.exists():
    env_file = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path=env_file)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse

from app.database.mongodb import db_manager
from app.routes.identify import router as identify_router
from app.routes.plants import router as plants_router
from app.routes.search import router as search_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ayurscan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    logger.info("Initializing AyurScan service...")
    db_manager.connect()
    yield
    # Shutdown: Close connections
    logger.info("Shutting down AyurScan service...")
    db_manager.close()

app = FastAPI(
    title="AyurScan API",
    description="AI-powered Ayurvedic plant identification and knowledge platform powered by Google Gemini and MongoDB.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration - production ready
origins_str = os.getenv("CORS_ORIGINS", "")
allowed_origins = [o.strip() for o in origins_str.split(",") if o.strip()]
is_wildcard = ("*" in allowed_origins) or (not allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if is_wildcard else allowed_origins,
    allow_credentials=not is_wildcard,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(identify_router)
app.include_router(plants_router)
app.include_router(search_router)

@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint showing service status and configuration readiness."""
    has_gemini_key = bool(os.getenv("GEMINI_API_KEY", "").strip())
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))

    return {
        "status": "healthy",
        "service": "AyurScan",
        "version": "1.0.0",
        "gemini_ready": has_gemini_key,
        "gemini_model": model_name,
        "confidence_threshold": threshold,
        "database": {
            "type": "mongodb" if db_manager.is_connected else "local_catalog_fallback",
            "connected": db_manager.is_connected
        }
    }

# Mount Frontend static directory for full-stack serving when available
frontend_dir = BASE_DIR.parent / "frontend"
if not frontend_dir.exists():
    frontend_dir = BASE_DIR / "frontend"

if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    # Serve index.html at root
    @app.get("/", include_in_schema=False)
    def serve_index():
        return FileResponse(str(frontend_dir / "index.html"))

    # Serve specific html files if requested directly from root
    @app.get("/{page}.html", include_in_schema=False)
    def serve_html_page(page: str):
        target = frontend_dir / f"{page}.html"
        if target.exists():
            return FileResponse(str(target))
        return JSONResponse(status_code=404, content={"detail": "Page not found"})

    # Mount entire frontend at root for css/js/assets
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend_root")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
