"""FastAPI backend for Lebo BI Dashboard."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Pre-import mock_data to trigger deterministic generation at startup
import backend.mock_data  # noqa: F401

from backend.routers import (
    metrics,
    brands,
    regional,
    retention,
    funnel,
    channels,
    content,
    realtime,
    export,
)

app = FastAPI(title="Lebo BI Dashboard API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Routers ----------
app.include_router(metrics.router)
app.include_router(brands.router)
app.include_router(regional.router)
app.include_router(retention.router)
app.include_router(funnel.router)
app.include_router(channels.router)
app.include_router(content.router)
app.include_router(realtime.router)
app.include_router(export.router)

# ---------- Frontend static files ----------
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIST.is_dir():
    # Serve bundled assets (JS/CSS/images)
    app.mount(
        "/assets",
        StaticFiles(directory=str(FRONTEND_DIST / "assets")),
        name="assets",
    )

    @app.get("/{full_path:path}")
    async def spa_fallback(request: Request, full_path: str):
        """SPA catch-all: serve index.html for any non-API route."""
        # Skip API and WebSocket paths
        if full_path.startswith("api/") or full_path.startswith("ws/"):
            return JSONResponse({"error": "not found"}, status_code=404)
        file = FRONTEND_DIST / full_path
        if file.is_file():
            return FileResponse(str(file))
        return FileResponse(str(FRONTEND_DIST / "index.html"))

else:

    @app.get("/")
    async def no_frontend():
        return JSONResponse(
            {
                "message": "Backend is running. Build the frontend first: cd frontend && npm run build"
            }
        )


if __name__ == "__main__":
    import uvicorn

    from backend.config import PORT

    uvicorn.run("backend.main:app", host="0.0.0.0", port=PORT, reload=True)
