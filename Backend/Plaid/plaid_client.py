import os
import plaid
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.api import plaid_api
from dotenv import load_dotenv
load_dotenv()
# from plaid.environments import Sandbox, Development, Production

def get_plaid_client():
    env = os.getenv("PLAID_ENV")
    # print(env)
    secret = None
    if env == "sandbox":
        host = plaid.Environment.Sandbox
        secret = os.getenv("PLAID_SECRET_SAND")
    elif env == "production":
        host = plaid.Environment.Production
        secret = os.getenv("PLAID_SECRET_PROD")

    # host = {
    #     "sandbox": "Sandbox",
    #     "development": "Development",
    #     "production": "Production",
    # }[env]

    configuration = Configuration(
        host=host,
        api_key={
            "clientId": os.getenv("PLAID_CLIENT_ID"),
            "secret": secret,
        },
    )
    api_client = ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)
# get_plaid_client()
