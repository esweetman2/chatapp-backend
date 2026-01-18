from sqlmodel import SQLModel, Field, Relationship, Session, text
from typing import Optional, List
from datetime import datetime, timezone
from Backend.db import engine
import time


# CREATE TABLE plaiditems (
#     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     project TEXT NOT NULL,
#     created_date TIMESTAMPTZ NOT NULL DEFAULT NOW()
#     updated_date TIMESTAMPTZ NOT NULL DEFAULT NOW()
# );

class PlaidModel(SQLModel, table=True):
    __tablename__ = "plaiditems"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True)
    item_id: str
    access_token: str
    institution_id: str
    status: str
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PlaidAccountModel(SQLModel, table=True):
    __tablename__ = "plaidaccounts"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True)
    account_id: str = Field(unique=True)
    balances: float
    name: str
    official_name: str
    institution_name: str
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))