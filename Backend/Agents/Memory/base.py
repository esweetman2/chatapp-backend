# Agents/memory/base.py
from abc import ABC, abstractmethod

class MemoryStrategy(ABC):
    @abstractmethod
    def get_memories(self, query: str,memory_table: str, top_k=10) -> list[str]:
        pass

class NoMemory(MemoryStrategy):
    def get_memories(self, query: str, memory_table: str, top_k=10):
        return []

class VectorMemory(MemoryStrategy):
    def __init__(self, memory_db, agent_id: int):
        self.db = memory_db
        self.agent_id = agent_id

    def get_memories(self, query: str, memory_table: str, top_k=10):
        return self.db.search_memory(
            query=query,  
            memory_table=memory_table, 
            agent_id=self.agent_id,
            top_k=top_k
        )

class MemoryFactory:
    def create_memory_strategy(self,agent_id: int, use_memory: bool, memory_db):
        if use_memory:
            return VectorMemory(memory_db, agent_id)
        else:
            return NoMemory()
