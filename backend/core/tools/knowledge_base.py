"""Knowledge base and vector store tools."""
from typing import Optional
from langchain.tools import tool
from langchain_core.documents import Document
from backend.services.vector_service import VectorService

@tool
async def search_knowledge_base(query: str) -> str:
    """📚 Knowledge Base & Document Search"""
    vector_service = VectorService()
    docs = await vector_service.search(query)
    
    if not docs:
        return "No specific information found in the knowledge base."
    
    results = "\n\n".join([f"Source Content: {doc.page_content}" for doc in docs])
    return f"Found the following information:\n{results}"

@tool
async def save_to_knowledge_base(content: str, metadata_category: str = "general") -> str:
    """💾 Save Information Tool"""
    try:
        vector_service = VectorService()
        doc = Document(page_content=content, metadata={"category": metadata_category})
        await vector_service.add_documents([doc])
        return "Successfully saved to knowledge base."
    except Exception as e:
        return f"Failed to save: {str(e)}"