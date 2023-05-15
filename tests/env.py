import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ["HOST"]
# host = os.environ["LOCALHOST"]

account_one_address = os.environ["ACCOUNT1_ADDRESS"]
account_one_memonic = os.environ["ACCOUNT1_MNEMONIC"]

account_two_address = os.environ["ACCOUNT2_ADDRESS"]
account_two_memonic = os.environ["ACCOUNT2_MNEMONIC"]