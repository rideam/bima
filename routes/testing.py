import json

from algosdk import mnemonic
from algosdk.account import address_from_private_key
from flask import Blueprint
from flask import request, jsonify

from algod import send_txn

testing_bp = Blueprint(
    'testing_bp',
    __name__
)


@testing_bp.route('/transactiontest', methods=['POST','GET'])
def transactiontest():
    """ Route to allow transaction testing. Simulates user joining policy and policy details being stored onchain """
    data = request.get_json()
    policy_details_dict = {
        'policy': 'Testing Policy',
        'description': 'Policy to test the transaction capacity of system',
        'period': f'2023-02-20 to 2023-12-31',
        'coverage_amount': 0.3,
        'strike_event': 'Temp > 50.0 C; Humidity > 75.0%; Moisture < 5.0 %',
        'signature': f'Joined by {data["wallet"]}'
    }
    success, txid = send_txn(
        address_from_private_key(mnemonic.to_private_key(data["passphrase"])),
        0,
        'CMAWFS52CTXLO7GNJNE2VKENRIT7W64QR2JJBQKJCZVUDBTUFZT2IXDJBI',
        json.dumps(policy_details_dict),
        mnemonic.to_private_key(data["passphrase"])
    )
    return jsonify({
        'status': success,
        'txid': txid
    })