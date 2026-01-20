from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from Backend.Plaid.plaid_client import get_plaid_client
from Backend.Models.PlaidModel import PlaidTransactionsModel
import json

class PlaidTransactions:
    def __init__(self):
        self.plaid_client = get_plaid_client()

    def get_transactions(self, access_tokens: list, user_id: str):
        # print("Access Tokens: ", access_tokens)
        access_token_list = []

        for i in access_tokens:
            access_token_list.append(i)
        
        results = []
        for token in access_token_list:

            request = TransactionsSyncRequest(access_token=token)
            resp = self.plaid_client.transactions_sync(request)
            res_dict = resp.to_dict()
            # results.append(res_dict)
            # return resp.to_dict()
            plaid_transaction_model = self._organize_transactions_response(res_dict, user_id)
            results.extend(plaid_transaction_model)

        return results
    
    def _organize_transactions_response(self, transactions: any, user_id: int):
        result = []
        transactions = transactions["added"]
        for transaction in transactions:

            counterparty = None
            counterparty_id = None
            counterparty_type = None

            if len(transaction["counterparties"]) > 0:
                counterparty = transaction["counterparties"][0]["name"]
                counterparty_id = transaction["counterparties"][0]["entity_id"]
                counterparty_type = transaction["counterparties"][0]["type"]
                
            transaction_model = PlaidTransactionsModel(
                user_id=int(user_id),
                account_id=transaction["account_id"],
                amount=transaction["amount"],
                authorized_date=transaction["authorized_date"],
                category=transaction["category"],
                counterparty=counterparty,
                counterparty_id=counterparty_id,
                counterparty_type=counterparty_type,
                date=transaction["date"],
                pending=transaction["pending"],
                transaction_id=transaction["transaction_id"]
            )

            result.append(transaction_model)
        
        return result
        

# if __name__ == "__main__":
#     _PlaidTransactions = PlaidTransactions()
#     trans = _PlaidTransactions.get_transactions(["access-sandbox-563a20d4-a58f-48ac-bd14-79d5ba71cc72"], 1)
#     print(trans)