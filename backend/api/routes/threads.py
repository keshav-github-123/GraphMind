
import logging
from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import ThreadListResponse, ChatHistoryResponse, DeleteThreadResponse
from backend.services.thread_service import ThreadService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", response_model=ThreadListResponse)
async def get_threads():
    """Get all conversation threads."""
    try:
        thread_service = ThreadService()
        threads = await thread_service.get_all_threads()
        logger.info(f"Retrieved {len(threads)} threads")
        return ThreadListResponse(threads=threads)
    except Exception as e:
        logger.error(f"Error fetching threads: {e}", exc_info=True)
        return ThreadListResponse(threads=[], error=str(e))


@router.get("/history/{thread_id}", response_model=ChatHistoryResponse)
async def get_thread_history(thread_id: str):
    """Get chat history for a specific thread."""
    try:
        from backend.main import app
        graph_manager = app.state.graph_manager
        
        raw_messages = await graph_manager.get_thread_history(thread_id)
        
        # Filter logic:
        # 1. Keep all USER messages.
        # 2. Keep ASSISTANT messages that have actual text content.
        # 3. Discard internal tool outputs (JSON strings) and empty tool-call markers.
        filtered_messages = []
        for msg in raw_messages:
            # Skip messages with no content (often sent during tool triggering)
            if not msg.content or msg.content.strip() == "":
                continue
            
            # Skip raw JSON/Tool output (like the date tool output in your logs)
            # We assume valid AI answers don't look like raw JSON objects
            content_stripped = msg.content.strip()
            if content_stripped.startswith('{') and content_stripped.endswith('}'):
                continue
                
            # Optional: Skip "Found the following information" style RAG snippets 
            # if you only want the final synthesized answer.
            if content_stripped.startswith('Found the following information:'):
                continue

            filtered_messages.append(msg)

        logger.info(f"Filtered {len(raw_messages)} down to {len(filtered_messages)} for thread {thread_id[:8]}")
        return ChatHistoryResponse(messages=filtered_messages)
        
    except Exception as e:
        logger.error(f"Error getting history for {thread_id}: {e}", exc_info=True)
        return ChatHistoryResponse(messages=[], error=str(e))