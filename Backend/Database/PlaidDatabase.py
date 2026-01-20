from sqlmodel import SQLModel, Field, select, func
# from sqlalchemy import Column
from sqlalchemy import text
# from pgvector.sqlalchemy import Vector
from openai import OpenAI
from Backend.db import engine, Session
from typing import Optional
from datetime import timezone
from dotenv import load_dotenv
from Backend.Models.PlaidModel import PlaidModel, PlaidAccountModel, PlaidTransactionsModel
import os
load_dotenv()


class PlaidDatabase:
    def __init__(self, db: Session):
        self.db = db

    def store_access_token(self, 
                           user_id: int, 
                           item_id: str,
                           access_token: str,
                           institution_id: str,
                        #    status: str | None
                           ):
        new_access_token = PlaidModel(
            user_id = user_id, 
                           item_id = item_id,
                           access_token = access_token,
                           institution_id = institution_id,
                        #    status = status
                           )
        self.db.add(new_access_token)
        self.db.commit()
        self.db.refresh(new_access_token)
        return {"message", "Access token saved."}
    
    def get_access_token(self, user_id: int):
        if user_id is None:
            return {"message": "No user id."}
        plaid_item = self.db.exec(select(PlaidModel).where(PlaidModel.user_id == user_id)).all()


        return plaid_item if plaid_item else None
    
    def add_plaid_accounts(self, accounts):
        try:
            self.db.add_all(accounts)
            self.db.commit()
            for account in accounts:
                self.db.refresh(account)
            
            return accounts
        except Exception as e:
            return str(e)
    
    def get_accounts(self, user_id:int):
        try:
            if user_id is None:
                return {"message": "No user id."}
            plaid_accounts = self.db.exec(select(PlaidAccountModel).where(PlaidAccountModel.user_id == user_id)).all()
            totals = [(account.balances) * -1 if account.type == "credit" else account.balances for account in plaid_accounts]
            total_balance = sum(totals)
            

            return {"accounts": plaid_accounts, "total_balances": total_balance}
        except Exception as e:
            return str(e)
    
    def get_transactions(self, user_id: str):
        try:
            if user_id is None:
                return {"message": "No user id."}
            plaid_accounts = self.db.exec(select(PlaidTransactionsModel).where(PlaidTransactionsModel.user_id == user_id)).all()
            # totals = [(account.balances) * -1 if account.type == "credit" else account.balances for account in plaid_accounts]
            # total_balance = sum(totals)
            

            return {"accounts": plaid_accounts, "total_balances": 0}
        except Exception as e:
            return str(e)
    
    def store_transactions(self, transactions: list):
        try:
            self.db.add_all(transactions)
            self.db.commit()
            for transaction in transactions:
                self.db.refresh(transaction)
            
            return transactions
        except Exception as e:
            return str(e)


