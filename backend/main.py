"""Refactored FastAPI application."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import chat, threads, upload
from backend.config import settings
from backend.core.graph import GraphManager
from backend.services.thread_service import ThreadService
from backend.utils.logger import setup_logging
from backend.utils.patches import apply_aiosqlite_patch

setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting application...")
    apply_aiosqlite_patch()
    
    thread_service = ThreadService()
    await thread_service.initialize_database()
    
    graph_manager = GraphManager()
    await graph_manager.initialize()
    app.state.graph_manager = graph_manager
    
    yield
    
    await graph_manager.cleanup()
    logger.info("✓ Cleanup completed")

app = FastAPI(title="LangGraph Chatbot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/ws", tags=["WebSocket"])
app.include_router(threads.router, prefix="/threads", tags=["Threads"])
app.include_router(upload.router, tags=["Upload"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)