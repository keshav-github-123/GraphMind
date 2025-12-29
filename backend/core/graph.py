"""Refactored LangGraph manager."""
import logging
from typing import List, Dict, Any, AsyncIterator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import TypedDict, Annotated
from backend.config import settings
from backend.core.tools import *
from backend.models.schemas import Message, MessageRole

logger = logging.getLogger(__name__)

class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

class GraphManager:
    def __init__(self):
        self.graph = None
        self.saver = None
        self.saver_context = None
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            streaming=settings.llm_streaming,
            temperature=settings.llm_temperature
        )
        self.mcp_client = MultiServerMCPClient({
            "expense": {"transport": "sse", "url": settings.mcp_expense_url}
        })
    
    async def initialize(self) -> None:
        logger.info("Initializing LangGraph...")
        self.saver_context = AsyncSqliteSaver.from_conn_string(settings.db_path)
        self.saver = await self.saver_context.__aenter__()
        all_tools = await self._load_tools()
        self.graph = await self._compile_graph(all_tools)
        logger.info(f"✓ Graph initialized with {len(all_tools)} tools")
    
    async def cleanup(self) -> None:
        if self.saver_context:
            await self.saver_context.__aexit__(None, None, None)
    
    async def _load_tools(self) -> List:
        local_tools = [
            search_tool, get_stock_price, calculator, percentage_calc,
            get_system_time, search_knowledge_base, save_to_knowledge_base
        ]
        try:
            remote_tools = await self.mcp_client.get_tools()
            logger.info(f"✓ Loaded {len(remote_tools)} MCP tools")
        except Exception as e:
            logger.warning(f"Could not load MCP tools: {e}")
            remote_tools = []
        return local_tools + remote_tools
    
    async def _compile_graph(self, tools: List) -> Any:
        llm_with_tools = self.llm.bind_tools(tools)
        
        async def chat_node(state: ChatState):
            response = await llm_with_tools.ainvoke(state["messages"])
            return {"messages": [response]}
        
        tool_node = ToolNode(tools)
        workflow = StateGraph(ChatState)
        workflow.add_node("chat_node", chat_node)
        workflow.add_node("tools", tool_node)
        workflow.add_edge(START, "chat_node")
        workflow.add_conditional_edges("chat_node", tools_condition)
        workflow.add_edge("tools", "chat_node")
        return workflow.compile(checkpointer=self.saver)
    
    async def stream_response(self, message: str, thread_id: str) -> AsyncIterator[Dict[str, Any]]:
        config = {"configurable": {"thread_id": thread_id}}
        async for event in self.graph.astream_events(
            {"messages": [HumanMessage(content=message)]}, config, version="v2"
        ):
            event_kind = event["event"]
            if event_kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield {"type": "token", "content": content}
            elif event_kind == "on_tool_start":
                yield {"type": "tool_start", "name": event.get("name", "unknown")}
            elif event_kind == "on_tool_end":
                yield {"type": "tool_end", "name": event.get("name", "unknown")}
    
    async def get_thread_history(self, thread_id: str) -> List[Message]:
        config = {"configurable": {"thread_id": thread_id}}
        state = await self.graph.aget_state(config)
        messages = []
        for msg in state.values.get("messages", []):
            role = MessageRole.USER if isinstance(msg, HumanMessage) else MessageRole.ASSISTANT
            messages.append(Message(role=role, content=msg.content))
        return messages
    
    async def is_first_message(self, thread_id: str) -> bool:
        try:
            config = {"configurable": {"thread_id": thread_id}}
            checkpoint_tuple = await self.saver.aget_tuple(config)
            return checkpoint_tuple is None
        except Exception:
            return True

