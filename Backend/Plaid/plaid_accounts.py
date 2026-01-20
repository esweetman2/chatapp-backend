from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from Backend.Plaid.plaid_client import get_plaid_client
from Backend.Models.PlaidModel import PlaidAccountModel
import json

class PlaidAccounts:
    def __init__(self):
        self.plaid_client = get_plaid_client()

    def get_accounts(self, access_tokens: list, user_id: str):
        # print("Access Tokens: ", access_tokens)
        results = []
        for token in access_tokens:

            request = AccountsGetRequest(access_token=token)
            resp = self.plaid_client.accounts_get(request)
            # results.append(resp.to_dict())
            # return resp.to_dict()
            plaid_account_model = self._organize_accounts_response(resp.to_dict(), user_id)
            results.extend(plaid_account_model)

        return results
    
    def _organize_accounts_response(self, accounts: dict, user_id: str):
        # print(accounts)
        # for i in accounts:
        #     if i == "item":
        #         print(accounts[i])
        #         print(accounts[i]["institution_name"])
        #     print("\n\n")
        # return accounts
        # with open("Testing\\ProductionScripts.py\\accounts_json_with_investments.json", 'w') as json_file:
        #     json.dump(accounts, json_file, indent=4)

        result = []
        institution_name = accounts["item"]["institution_name"]
        accounts_list = accounts["accounts"]
        for i in accounts_list:

            official_name = i["official_name"] if i["official_name"] else ""

            temp = PlaidAccountModel(
                user_id=int(user_id),
                account_id=i["account_id"],
                balances=i["balances"]["current"],
                name=i["name"],
                official_name=official_name,
                type=i["type"],
                subtype=i["subtype"],
                institution_name=institution_name
            )

            result.append(temp)
        
        return result

