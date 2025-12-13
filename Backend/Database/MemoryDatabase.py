from sqlmodel import SQLModel, Field, select
# from sqlalchemy import Column
from sqlalchemy import text
# from pgvector.sqlalchemy import Vector
from openai import OpenAI
from Backend.db import engine, Session
from typing import Optional
from datetime import timezone
from dotenv import load_dotenv
from Backend.Models.MemoryModel import AgentMemoryModel
import os
load_dotenv()

class MemoryDatabase:
    def __init__(self, db: Session):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.db = db
        
    def _get_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def search_memory(self, query: str,  memory_table: str, agent_id: int, top_k=10):
        try:
            query_embedding = self._get_embedding(query)
            embedding_str = f"[{', '.join(map(str, query_embedding))}]"
            # with Session(engine) as session:
            sql = text(f"""
                SELECT id, memory_text, embedding <#> CAST(:embedding AS vector) AS score
                FROM {str(memory_table)}
                WHERE agent_id = {str(agent_id)}
                ORDER BY embedding <#> CAST(:embedding AS vector)
                LIMIT :top_k
            """)
            params = {
                "embedding": embedding_str,
                "top_k": top_k
            }
            results = self.db.exec(sql,params=params)
            res = results.fetchall()
            print(res)
            return res
        except Exception as e:
            return str(e)
    
    def store_memory(self, memory_text: str, user_id: int, agent_id: int):
        try:
            embedding = self._get_embedding(memory_text)
            new_memory = AgentMemoryModel(
                agent_id=agent_id,
                user_id=user_id,
                memory_text=memory_text,
                embedding=embedding
            )
            self.db.add(new_memory)
            self.db.commit()
            
            return new_memory
        except Exception as e:
            return str(e)
        # with Session(engine) as session:
        #     session.add(new_memory)
        #     session.commit()
        #     return {"memory": memory_text}
        
        # return "error"