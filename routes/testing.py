import json
import settings
import time

from algosdk import mnemonic
from algosdk.account import address_from_private_key
from flask import Blueprint
from flask import request, jsonify
from models import User

from algod import send_txn
from enum import Enum

testing_bp = Blueprint(
    'testing_bp',
    __name__
)

class Conditions(Enum):
    GT = '>'
    LS = '<'
    EQ = '='





@testing_bp.route('/joinpolicytest', methods=['POST','GET'])
def user_joining_policy_test():
    """ Route to allow transaction testing. Simulates user joining policy and policy details being stored onchain.
        Also allows testing how much time it takes to send data to the Algorand blockchain.
     """

    data = request.get_json()
    policy_details_dict = {
        'policy': 'Testing Policy',
        'description': 'Policy to test the transaction capacity of system',
        'period': f'2023-02-20 to 2023-12-31',
        'coverage_amount': 0.3,
        'strike_event': 'Temp > 50.0 C; Humidity > 75.0%; Moisture < 5.0 %',
        'signature': f'Joined by {data["wallet"]}'
    }

    start_time = time.time()
    success, txid = send_txn(
        address_from_private_key(mnemonic.to_private_key(data["passphrase"])),
        0,
        'CMAWFS52CTXLO7GNJNE2VKENRIT7W64QR2JJBQKJCZVUDBTUFZT2IXDJBI',
        json.dumps(policy_details_dict),
        mnemonic.to_private_key(data["passphrase"])
    )
    end_time = time.time()

    return jsonify({
        'status': success,
        'txid': txid,
        'elapsed_time': end_time - start_time
    })


@testing_bp.route('/payouttest', methods=['POST','GET'])
def payout_test():
    """ Route to allow testing of how long payouts take to be issued """
    admin = User(settings.account_one_memonic)

    data = request.get_json()
    weather_dict = {
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "soil_moisture": data["soil_moisture"],
        "farm": data["farm"],
        "crop": data["crop"],
        "user": data["wallet"]
    }

    event = {
        'temperature': 50,
        'temperature_condition': '>',
        'humidity': 65,
        'humidity_condition': '>',
        'soil_moisture': 5,
        'soil_moisture_condition': '<'
    }

    # send data to chain
    admin.send(0, data["wallet"],json.dumps(weather_dict))

    condition_pass = {
        'temperature': False,
        'humidity': False,
        'soil_moisture': False
    }


    # check strike conditions
    if event['temperature_condition'] == Conditions.GT.value:
        if data["temperature"] > event['temperature']:
            condition_pass['temperature'] = True
    elif event['temperature_condition'] == Conditions.LS.value:
        if data["temperature"] < event['temperature']:
            condition_pass['temperature'] = True

    # Humidity conditions
    if event['humidity_condition'] == Conditions.GT.value:
        if data["humidity"] > event['humidity']:
            condition_pass['humidity'] = True
    elif event['humidity_condition'] == Conditions.LS.value:
        if data["humidity"] < event['humidity']:
            condition_pass['humidity'] = True

    # Soil moisture
    if event['soil_moisture_condition'] == Conditions.GT.value:
        if data["soil_moisture"] > event['soil_moisture']:
            condition_pass['soil_moisture'] = True
    elif event['soil_moisture_condition'] == Conditions.LS.value:
        if data["soil_moisture"] < event['soil_moisture']:
            condition_pass['soil_moisture'] = True

    trigger_payout = all(value for value in condition_pass.values())

    payout_success = False
    if trigger_payout:
        success, txid = admin.send(0.1, data["wallet"],
                                   f'Paid by {admin.public_key}')
        payout_success = success
    return jsonify({ 'payout_success': payout_success})
