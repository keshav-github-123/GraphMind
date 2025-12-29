"""Document processing service."""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import settings
from backend.services.vector_service import VectorService

class DocumentService:
    def __init__(self):
        self.vector_service = VectorService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    async def process_pdf(self, file_path: Path) -> int:
        loader = PyPDFLoader(str(file_path))
        docs = loader.load()
        splits = self.text_splitter.split_documents(docs)
        await self.vector_service.add_documents(splits)
        return len(splits)
    
    def validate_file(self, filename: str) -> bool:
        return any(filename.lower().endswith(ext) for ext in settings.allowed_file_types)


