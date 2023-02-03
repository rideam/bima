from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client import indexer
import settings


def myindexer():
    """Initialise and return an indexer"""

    algod_address = settings.algod_indexer
    algod_token = settings.algod_api
    headers = {
        "X-API-Key": algod_token,
    }
    return indexer.IndexerClient("", algod_address, headers)


def get_transactions(address, substring):
    """Returns a list of transactions related to the given address"""
    response = myindexer().search_transactions(address=address, txn_type="pay")
    txns = []
    for txn in response["transactions"]:
        sender = txn["sender"]
        fee = txn["fee"]

        amount = txn["payment-transaction"]["amount"]
        if sender == address:

            # if the current account is the sender, add fee and display transaction as negative
            amount += fee
            amount *= -1
            other_address = txn["payment-transaction"]["receiver"]
        else:
            other_address = sender

        amount /= microalgos_to_algos_ratio

        # check for searched address
        if substring not in other_address:
            continue

        txns.append({"amount": amount, "address": other_address})
    return txns
