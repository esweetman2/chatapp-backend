from sqlmodel import SQLModel, Field, select
from sqlalchemy import Column
from sqlalchemy import text
from pgvector.sqlalchemy import Vector
import uuid
from Backend.db import engine, Session
from typing import Optional
from datetime import datetime, timezone
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

class ClientsMemory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    memory: str
    client: str
    embedding: Optional[list[float]] = Field(
        sa_column=Column(Vector(1536))
    )
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

SQLModel.metadata.create_all(engine)

class ClientsMemoryMangement:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def store_memory(self, memory_text: str, client: str):
        from datetime import datetime
        embedding = self.get_embedding(memory_text)
        new_memory = ClientsMemory(
            memory=memory_text,
            client=client,
            embedding=embedding,
            created_at=datetime.now(timezone.utc)
        )
        with Session(engine) as session:
            session.add(new_memory)
            session.commit()
            return {"memory": memory_text}
        
        return "error"

    def search_memory(self, query: str,  memory_table: str, top_k=10):
        query_embedding = self.get_embedding(query)
        embedding_str = f"[{', '.join(map(str, query_embedding))}]"
        with Session(engine) as session:
            sql = text(f"""
                SELECT id, memory, embedding <#> CAST(:embedding AS vector) AS score
                FROM {str(memory_table)}
                ORDER BY embedding <#> CAST(:embedding AS vector)
                LIMIT :top_k
            """)
            params = {
                "embedding": embedding_str,
                "top_k": top_k
            }
            results = session.exec(sql,params=params)
            res = results.fetchall()
            return res

# if __name__ == "__main__":
#     _MemoryManagement = ClientsMemoryMangement()
    
#     _MemoryManagement.store_memory(memory_text="Currently need to run classification test on new documents.", client="Novum")

    # _MemoryManagement.store_memory(memory_text="The wedding venue is at **The Equinox Golf Resort & Spa")
    
    # _MemoryManagement.store_memory(memory_text="The wedding is on February 15th, 2026")
    
    # _MemoryManagement.store_memory(memory_text="The address of the Equinox is 3567 Main St, Manchester, VT 05254")
    
    # _MemoryManagement.store_memory(memory_text="The ceremony will be at the First Congregational Church in Manchester, Vermont")
    
    # _MemoryManagement.store_memory(memory_text="The church's address is 3624 Main St, Manchester, VT 05254")
    
    # _MemoryManagement.store_memory(memory_text="The ceremony will start at 4 PM EST and the reception/cocktail will start 5 PM EST in teh colonnade room.")
    
    # _MemoryManagement.store_memory(memory_text="The dress attire will be black tie optional.")
    
    # _MemoryManagement.store_memory(memory_text="The after party will be at the Meadow House and will be optional.")

    # _MemoryManagement.store_memory(memory_text="The church is within walking distance of the Equinox.")
    
    # _MemoryManagement.store_memory(memory_text="On Friday there will be an apre ski event for anyone who might be in town.")