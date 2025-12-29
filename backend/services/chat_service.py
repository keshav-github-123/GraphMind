"""Chat service for message handling."""
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from backend.config import settings

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            streaming=settings.llm_streaming,
            temperature=settings.llm_temperature
        )
    
    async def generate_summary(self, first_message: str, max_words: int = 6) -> str:
        try:
            prompt = f"Generate a short title (max {max_words} words) for: {first_message}. Return ONLY the text."
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return response.content.strip().strip('"')
        except Exception as e:
            print(f"Error generating summary: {e}")
            return first_message[:30] + "..."