"""WebSocket chat endpoint."""
import logging
import json
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.models.schemas import ChatMessageRequest, WebSocketMessageType
from backend.services.chat_service import ChatService
from backend.services.thread_service import ThreadService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for chat interactions."""
    await websocket.accept()
    logger.info("🔌 WebSocket client connected")
    
    # Access graph_manager through websocket.app.state
    graph_manager = websocket.app.state.graph_manager
    chat_service = ChatService()
    thread_service = ThreadService()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Validate request
            try:
                request_model = ChatMessageRequest(**message_data)
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Invalid request: {str(e)}"
                })
                continue
            
            user_message = request_model.message
            thread_id = request_model.thread_id or str(uuid.uuid4())
            
            logger.info(f"📨 Message: '{user_message[:50]}...' | Thread: {thread_id[:8]}")
            
            # Send thread ID
            await websocket.send_json({
                "type": "thread_id",
                "thread_id": thread_id
            })
            
            # Check if first message
            is_first_message = await graph_manager.is_first_message(thread_id)
            
            # Stream response
            token_count = 0
            async for event in graph_manager.stream_response(user_message, thread_id):
                event_type = event.get("type")
                
                if event_type == "token":
                    token_count += 1
                    await websocket.send_json(event)
                
                elif event_type == "status":
                    await websocket.send_json(event)
                
                elif event_type == "tool_start":
                    await websocket.send_json({
                        "type": "status",
                        "content": f"🔧 Calling tool: {event.get('name')}..."
                    })
                
                elif event_type == "tool_end":
                    await websocket.send_json({
                        "type": "status",
                        "content": f"✅ Tool {event.get('name')} completed"
                    })
            
            logger.info(f"✅ Response complete | Tokens: {token_count}")
            
            # Generate summary for first message
            if is_first_message:
                summary = await chat_service.generate_summary(user_message)
                await thread_service.create_thread_summary(thread_id, summary)
                logger.info(f"📝 Summary: '{summary}'")
            
            # Send completion
            await websocket.send_json({"type": "complete"})
    
    except WebSocketDisconnect:
        logger.info("🔌 Client disconnected")
    
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass