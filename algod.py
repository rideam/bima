from algosdk import account, mnemonic
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.transaction import PaymentTxn
from algosdk.v2client import algod
import settings


def algod_client():
    algod_address = settings.algod_api
    algod_token = settings.algod_api_key
    headers = {
        "X-API-Key": algod_token,
    }
    return algod.AlgodClient(algod_token, algod_address, headers)


def create_account():
    private_key, address = account.generate_account()
    return mnemonic.from_private_key(private_key)


def get_balance(address):
    account_info = algod_client().account_info(address)
    balance = account_info.get('amount') / microalgos_to_algos_ratio
    return balance


def send_txn(sender, quantity, receiver, note, sk):
    """Create and sign a transaction. Return transaction status and transaction id"""
    quantity = int(quantity * microalgos_to_algos_ratio)
    params = algod_client().suggested_params()
    note = note.encode()
    try:
        unsigned_txn = PaymentTxn(sender, params, receiver, quantity, None, note)
    except Exception as err:
        print(err)
        return False, ""
    signed_txn = unsigned_txn.sign(sk)
    try:
        txid = algod_client().send_transaction(signed_txn)
    except Exception as err:
        print(err)
        return False, ""

    try:
        wait_for_confirmation(txid, 4)
        return True, txid
    except Exception as err:
        print(err)
        return False, ""


def wait_for_confirmation(transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """

    start_round = algod_client().status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = algod_client().pending_transaction_info(transaction_id)
        except Exception as err:
            print(err)
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        algod_client().status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))
