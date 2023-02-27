import os
from dotenv import load_dotenv

load_dotenv()

configClass = os.getenv("CONFIG_CLASS", 'config.BaseConfig')
secret_key = os.environ["SECRET_FLASK"]

algod_api = os.environ["TESTNET_ALGOD_ADDRESS"]
algod_indexer = os.environ["TESTNET_ALGOINDEXER_SERVER"]
algod_api_key = os.environ["TESTNET_ALGOD_API_KEY"]

account_one_address = os.environ["ACCOUNT1_ADDRESS"]
account_one_memonic = os.environ["ACCOUNT1_MNEMONIC"]

account_two_address = os.environ["ACCOUNT2_ADDRESS"]
account_two_memonic = os.environ["ACCOUNT2_MNEMONIC"]

admin_user = os.environ["ADMIN_USERNAME"]
admin_pwd = os.environ["ADMIN_PASSWORD"]
admin_swatch = os.environ['ADMIN_SWATCH']

db_url = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
log_with_gunicorn = os.getenv('LOG_WITH_GUNICORN', default=False)

template_mode = 'bootstrap3'
