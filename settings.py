import os
from dotenv import load_dotenv

load_dotenv()

configClass = 'config.BaseConfig'
secret_key = os.environ["SECRET_FLASK"]

algod_api = os.environ["TESTNET_ALGOD_ADDRESS"]
algod_indexer = os.environ["TESTNET_ALGOINDEXER_SERVER"]
algod_api_key = os.environ["TESTNET_ALGOD_API_KEY"]

account_one_address = os.environ["ACCOUNT1_ADDRESS"]
account_one_memonic = os.environ["ACCOUNT1_MNEMONIC"]

account_two_address = os.environ["ACCOUNT2_ADDRESS"]
account_two_memonic = os.environ["ACCOUNT2_MNEMONIC"]
