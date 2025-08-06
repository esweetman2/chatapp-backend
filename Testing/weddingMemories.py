from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector
import uuid
from db import engine, Session
from typing import Optional
from datetime import datetime, timezone
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Memory(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    memory: str
    embedding: Optional[list[float]] = Field(
        sa_column=Column(Vector(1536))
    )
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

SQLModel.metadata.create_all(engine)
def store_memory(memory_text: str):
    from datetime import datetime
    embedding = get_embedding(memory_text)
    new_memory = Memory(
        memory=memory_text,
        embedding=embedding,
        created_at=datetime.now(timezone.utc)
    )
    with Session(engine) as session:
        session.add(new_memory)
        session.commit()

from sqlalchemy import text
def search_memory(query: str, top_k=5):
    query_embedding = get_embedding(query)
    embedding_str = f"[{', '.join(map(str, query_embedding))}]"
    with Session(engine) as session:
        sql = text("""
            SELECT id, memory, embedding <=> CAST(:embedding AS vector) AS score
            FROM memory
            ORDER BY embedding <#> CAST(:embedding AS vector)
            LIMIT :top_k
        """)
        results = session.execute(sql, {
            "embedding": embedding_str,
            "top_k": top_k
        })
        
        res = results.fetchall()
        return res




# store_memory("The wedding ceremony starts at 4 PM on February 15th, 2025.")
# store_memory("The reception begins at 6 PM at The Equinox.")
# store_memory("When is the ceremony?")
# store_memory("The ceremony is at 4PM on Februrary 15, 2025 and the reception will follow after at 6 PM at the equinox")
# store_memory("Ace is my dog")



matches = search_memory("What time should I be at the ceremony")

for row in matches:
    print(row[1])
    print(f"Score: ============ {row[2]} =============")
