from typing import List, Optional
import aiosqlite
from datetime import datetime
from backend.config import settings
from backend.models.schemas import ThreadSummary

class ThreadService:
    def __init__(self):
        self.db_path = settings.db_path
    
    async def create_thread_summary(self, thread_id: str, summary: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO thread_summaries 
                (thread_id, summary, created_at) VALUES (?, ?, ?)""",
                (thread_id, summary, datetime.utcnow().isoformat())
            )
            await db.commit()
    
    async def get_all_threads(self) -> List[ThreadSummary]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT thread_id, summary, created_at
                FROM thread_summaries ORDER BY created_at DESC"""
            )
            rows = await cursor.fetchall()
            return [
                ThreadSummary(thread_id=row[0], summary=row[1], created_at=row[2])
                for row in rows
            ]
    
    async def delete_thread(self, thread_id: str) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
                await db.execute("DELETE FROM thread_summaries WHERE thread_id = ?", (thread_id,))
                await db.commit()
                return True
        except Exception:
            return False
    
    async def initialize_database(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS thread_summaries (
                    thread_id TEXT PRIMARY KEY,
                    summary TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            await db.commit()
