from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import  Session
from Backend.db import  get_session
import os
import json

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from Backend.Database.PlaidDatabase import PlaidDatabase
# from plaid.model.link_token_create_request_language import LinkTokenCreateRequestLanguage

from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from Backend.Plaid.plaid_client import get_plaid_client
from Backend.Plaid.plaid_accounts import PlaidAccounts
from Backend.Plaid.plaid_transactions import PlaidTransactions

router = APIRouter()
plaid_client = get_plaid_client()

# --- Schemas ---
class CreateLinkTokenRequest(BaseModel):
    user_id: str  # your internal user id

class PublicTokenExchangeRequest(BaseModel):
    public_token: str
    user_id: str
    metadata: dict

@router.post("/plaid/create_link_token", tags=["Plaid"])
def create_link_token(req: CreateLinkTokenRequest):
    print(req)
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=req.user_id),
            client_name="My App",
            products=[Products("transactions")],  # adjust to your needs
            optional_products=[Products("investments")],
            country_codes=[CountryCode("US")],
            language="en",
            enable_multi_item_link=True 
            # redirect_uri=os.getenv("PLAID_REDIRECT_URI"),  # optional depending on institution/OAuth
            # webhook="https://your-api.com/plaid/webhook",  # optional but recommended
        )

        response = plaid_client.link_token_create(request)

        return {"link_token": response["link_token"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/plaid/exchange_public_token", tags=["Plaid"])
def exchange_public_token(req: PublicTokenExchangeRequest, session: Session = Depends(get_session)):
    print(req)
    print("")
    try:
        _PlaidDatabase = PlaidDatabase(session)
        exchange_request = ItemPublicTokenExchangeRequest(public_token=req.public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)

        institution_id = req.metadata["institution"]["institution_id"]

        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]

        saved_token = _PlaidDatabase.store_access_token(
            user_id=int(req.user_id), 
                           item_id=item_id,
                           access_token=access_token,
                           institution_id=institution_id,
                        #    status=None
        )

        return saved_token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


## THis route uses database
@router.get("/plaid/accounts", tags=["Plaid"])
def get_accounts(user_id: str, session: Session = Depends(get_session)):
    # TODO: load access_token from DB using user_id
    _PlaidDatabase = PlaidDatabase(session)
    accounts = _PlaidDatabase.get_accounts(user_id)
    
    return accounts
    

# ## THIS route uses API
@router.get("/plaid/load_accounts/plaidapi", tags=["Plaid"])
def get_accounts(user_id: str, session: Session = Depends(get_session)):
    # TODO: load access_token from DB using user_id
    _PlaidDatabase = PlaidDatabase(session)
    plaid_items = _PlaidDatabase.get_access_token(user_id)
    if not plaid_items:
        return []
    
    access_tokens = []

    for i in plaid_items:
        access_tokens.append(i.access_token)

    _PlaidAccounts = PlaidAccounts()
    accounts = _PlaidAccounts.get_accounts(access_tokens=access_tokens, user_id=user_id)
    _PlaidDatabase = PlaidDatabase(session)
    added_accounts = _PlaidDatabase.add_plaid_accounts(accounts=accounts)
    return added_accounts

@router.get("/plaid/load_transactions/plaidapi", tags=["Plaid"])
def get_transactions(user_id: int, session: Session = Depends(get_session)):
    # TODO: load access_token from DB using user_id
    _PlaidDatabase = PlaidDatabase(session)
    plaid_items = _PlaidDatabase.get_access_token(user_id)
    if not plaid_items:
        return []
    
    access_tokens = []

    for i in plaid_items:
        access_tokens.append(i.access_token)
    
    _PlaidTransactions = PlaidTransactions()
    transactions = _PlaidTransactions.get_transactions(access_tokens=access_tokens, user_id=user_id)
    # return transactions
    _PlaidDatabase = PlaidDatabase(session)
    added_transactions = _PlaidDatabase.store_transactions( transactions=transactions)

    return added_transactions

    # request = TransactionsSyncRequest(access_token=access_tokens[0])
    # resp = plaid_client.transactions_sync(request)
    # res_dict = resp.to_dict()

    # with open("Testing\\ProductionScripts.py\\transactions_json.json", 'w') as json_file:
    #     json.dump(res_dict, json_file, indent=4)
    # return resp.to_dict()