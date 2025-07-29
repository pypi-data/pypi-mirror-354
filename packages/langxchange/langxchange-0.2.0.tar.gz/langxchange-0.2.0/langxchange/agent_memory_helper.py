# langxchange/agent_memory_helper.py

import os
import sqlite3
import uuid
from datetime import datetime
from typing import List, Tuple, Optional

class AgentMemoryHelper:
    """
    Manages per-agent conversational memory using SQLite:
      - Stores every turn in SQLite (agent_id, timestamp, role, text)
      - Provides retrieval and basic search functionality
    """

    def __init__(
        self,
        llm_helper,
        sqlite_path: str = "agent_memory.db"
    ):
        # LLM helper must provide get_embedding(text)->List[float]
        if not hasattr(llm_helper, "get_embedding"):
            raise ValueError("llm_helper must implement .get_embedding(text)")

        self.llm = llm_helper

        # --- SQLite setup ---
        self.conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        self._init_sqlite()

    def _init_sqlite(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            agent_id TEXT,
            timestamp TEXT,
            role      TEXT,
            text      TEXT
        )""")
        self.conn.commit()

    def add_memory(self, agent_id: str, role: str, text: str):
        """Add a new message turn to SQLite for this agent."""
        timestamp = datetime.utcnow().isoformat()
        # Insert into SQLite
        self.conn.execute(
            "INSERT INTO memory (agent_id,timestamp,role,text) VALUES (?,?,?,?)",
            (agent_id, timestamp, role, text)
        )
        self.conn.commit()

    def get_recent(
        self,
        agent_id: str,
        n: int = 10
    ) -> List[Tuple[str, str, str]]:
        """
        Return the last n turns as a list of tuples:
          [(timestamp, role, text), ...], most recent last.
        """
        c = self.conn.cursor()
        c.execute("""
            SELECT timestamp, role, text
              FROM memory
             WHERE agent_id = ?
          ORDER BY timestamp DESC
             LIMIT ?
        """, (agent_id, n))
        rows = c.fetchall()
        return list(reversed(rows))

    def search_memory(
        self,
        agent_id: str,
        query: str,
        top_k: int = 5
    ) -> List[Tuple[str, str, str]]:
        """
        Perform a basic substring search over this agent's memory text.
        Returns up to top_k matching turns as (timestamp, role, text).
        """
        pattern = f"%{query}%"
        c = self.conn.cursor()
        c.execute("""
            SELECT timestamp, role, text
              FROM memory
             WHERE agent_id = ? AND text LIKE ?
          ORDER BY timestamp DESC
             LIMIT ?
        """, (agent_id, pattern, top_k))
        rows = c.fetchall()
        return list(reversed(rows))

    def clear_memory(self, agent_id: str):
        """Delete all history for the given agent."""
        self.conn.execute("DELETE FROM memory WHERE agent_id = ?", (agent_id,))
        self.conn.commit()
