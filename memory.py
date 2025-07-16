from sqlmodel import Session, select
from models import Conversation, Message, Users
from db import engine
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


def get_or_create_conversation(db: Session, user_id: str, id: int = 0) -> Conversation:
    print(f"Fetching conversation for user_id: {user_id}")
    # print(db, type(db))
    # with Session(engine) as session:
        # yield session
    user = db.exec(select(Users).where(Users.username == user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="user Not found."
        )
        
    result = db.exec(select(Conversation).where(Conversation.user_id == user_id).where(Conversation.id == id)).first()
    if result:
        return [ {"conversation" :result, "messages": result.messages} ]
    new_convo = Conversation(user_id=user_id)
    print("Adding new_convo", new_convo)
    db.add(new_convo)
    db.commit()
    db.refresh(new_convo)
    return [ {"conversation" :new_convo, "messages": new_convo.messages} ]
    # return new_convo


def get_conversation(db: Session, conversation_id: int, user_id: str) -> Optional[Conversation]:
    # with Session(engine) as session:
    convo = db.exec(select(Conversation).where(Conversation.id == conversation_id).where(Conversation.user_id == user_id)).first()
    if convo:
        return convo
    else:
        return "Conversation not found"
    
def get_conversations(db: Session, user_id: str) -> Optional[Conversation]:
    # with Session(engine) as session:
    convo = db.exec(select(Conversation).where(Conversation.user_id == user_id)).fetchall()
    if convo:
        return convo
    else:
        return []
    

def updateConversatinSummary(db: Session, conversation_id: int, summary: str) -> Conversation:
    # with Session(engine) as session:
    convo = db.exec(select(Conversation).where(Conversation.id == conversation_id)).first()
    if convo:
        convo.summary = summary
        db.add(convo)
        db.commit()
        db.refresh(convo)
        return convo
    else:
        raise ValueError("Conversation not found")

def get_conversation_messages(db: Session, conversation_id: int) -> list[Message]:
    # with Session(engine) as db:
    return db.exec(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
    ).all()

def add_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    # with Session(engine) as session:
    try:
        msg = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg
    except SQLAlchemyError as e:
        db.rollback()
        # Log the error here if desired
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def check_convo(db: Session, conversation_id: int, user_id: str) -> Conversation:
    # with Session(engine) as session:
    convo = db.exec(
        select(Conversation).where(Conversation.id == conversation_id).where(Conversation.user_id == user_id)).first()
    if convo is None:
        return None
    return [ {"conversation" :convo, "messages": convo.messages} ]