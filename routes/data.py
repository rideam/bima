import json

from flask import Blueprint
from models import Weather, \
    PremiumPayments, \
    Farm, \
    User, \
    Event, \
    Payout, \
    Policy, \
    PoliciesFarmers, \
    db
from flask import request, jsonify
from flask_login import current_user
import datetime
import settings
from sqlalchemy import desc

from enum import Enum

data_bp = Blueprint(
    'data_bp',
    __name__
)


class Conditions(Enum):
    GT = '>'
    LS = '<'
    EQ = '='


@data_bp.route('/weather', methods=['POST', 'GET'])
def add_weather_data():
    admin = User(settings.account_one_memonic)

    if request.method == 'POST':
        data = request.get_json()
        weather_dict = {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "soil_moisture": data["soil_moisture"],
            "farm": data["farm"],
            "crop": data["crop"],
            "user": data["user"]
        }

        # farm = Farm.query.filter_by(name=data['farm']).first()
        # user = User.query.filter(User.farms.contains(farm)).first()
        user = User.query.filter_by(wallet_address=data['user']).first()
        user_policy = Policy.query.filter(Policy.farmers.contains(user)).first()
        w_success, w_txid = admin.send(0, user.wallet_address,
                                       json.dumps(weather_dict))

        if w_success:
            print(f'data send to chain \n https://goalseeker.purestake.io/algorand/testnet/transaction/{w_txid}')
            weather_dict["blockchain_url"] = f'https://goalseeker.purestake.io/algorand/testnet/transaction/{w_txid}'

        weather_rec = Weather(**weather_dict)
        db.session.add(weather_rec)
        db.session.commit()
        strike_events = user_policy.strike_event

        condition_pass = {
            'temperature': False,
            'humidity': False,
            'soil_moisture': False,
            'policy_is_valid': user_policy.is_valid(datetime.datetime.now(), data['user'])
        }
        # trigger_payout = False
        for event in strike_events:
            # Temperature conditions
            if event.temperature_condition == Conditions.GT.value:
                if data["temperature"] > event.temperature:
                    condition_pass['temperature'] = True
            elif event.temperature_condition == Conditions.LS.value:
                if data["temperature"] < event.temperature:
                    condition_pass['temperature'] = True

            # Humidity conditions
            if event.humidity_condition == Conditions.GT.value:
                if data["humidity"] > event.humidity:
                    condition_pass['humidity'] = True
            elif event.humidity_condition == Conditions.LS.value:
                if data["humidity"] < event.humidity:
                    condition_pass['humidity'] = True

            # Soil moisture
            if event.soil_moisture_condition == Conditions.GT.value:
                if data["soil_moisture"] > event.soil_moisture:
                    condition_pass['soil_moisture'] = True
            elif event.soil_moisture_condition == Conditions.LS.value:
                if data["soil_moisture"] < event.soil_moisture:
                    condition_pass['soil_moisture'] = True

        trigger_payout = all(value for value in condition_pass.values())
        print(f'Trigger payout {trigger_payout}')
        if trigger_payout:
            success, txid = admin.send(user_policy.coverage_amount, user.wallet_address,
                                       f'Paid by {admin.public_key}')

            # print(success)
            # print(f'https://goalseeker.purestake.io/algorand/testnet/transaction/{txid}')

            if success:
                pyt_dict = {
                    'farmer_id': user.wallet_address,
                    'policy_id': user_policy.id,
                    'amount': user_policy.coverage_amount,
                    'blockchain_url': f'https://goalseeker.purestake.io/algorand/testnet/transaction/{txid}'
                }
                payout = Payout(**pyt_dict)
                db.session.add(payout)
                db.session.commit()

        return jsonify(weather_rec.as_dict())

    elif request.method == 'GET':
        weather_recs = Weather.query.all()
        return jsonify([weather.as_dict() for weather in weather_recs])


@data_bp.route('/policies', methods=['POST', 'GET', 'DELETE'])
def policies():
    if request.method == 'GET':
        # Get all policy records
        policy_recs = Policy.query.all()
        return jsonify([{**policy.as_dict(), 'strike_event': policy.strike_event[0].desc,
                         'myPolicy': policy.my_policy(current_user.public_key)} for policy in policy_recs])

    if request.method == 'POST':
        # Join policy
        id = request.json
        policy_to_join = Policy.query.filter_by(id=int(id)).one()
        user = User.query.filter_by(wallet_address=current_user.public_key).first()

        if user not in policy_to_join.farmers:
            policy_details_dict = {
                'policy': policy_to_join.name,
                'description': policy_to_join.description,
                'period': f'{policy_to_join.start_date} to {policy_to_join.end_date}',
                'coverage_amount': policy_to_join.coverage_amount,
                'strike_event': policy_to_join.strike_event[0].desc,
                'signature': f'Joined by {current_user.public_key}'
            }

            success, txid = current_user.send(0, policy_to_join.receiver, json.dumps(policy_details_dict))
            if success:
                policy_to_join.farmers.append(user)
                db.session.commit()

                try:
                    policy_farmer_rec = PoliciesFarmers.query.filter_by(policy_id=policy_to_join.id,
                                                                        farmer_id=current_user.public_key).first()
                    policy_farmer_rec.blockchain_url = f'https://goalseeker.purestake.io/algorand/testnet/transaction/{txid}'
                    db.session.flush()
                    db.session.commit()
                    # print(f'https://goalseeker.purestake.io/algorand/testnet/transaction/{txid}')

                except Exception as err:
                    print(err)
            else:
                print("trans failed")
                return jsonify({
                    "msg": "Please fund your account with algos to join policy",
                    "class": "alert-danger"
                })
        # policy_recs = Policy.query.all()
        # return jsonify([{**policy.as_dict(),
        #                  'strike_event': policy.strike_event[0].desc,
        #                  'myPolicy': policy.my_policy(current_user.public_key)} for policy in policy_recs]
        #                )
        return jsonify({
            "msg": "Enrolled in policy",
            "class": "alert-success"
        })

    if request.method == 'DELETE':
        # Remove enrollment from policy
        id = request.json
        policy_to_cancel = Policy.query.filter_by(id=int(id)).one()
        user = User.query.filter_by(wallet_address=current_user.public_key).first()

        if user in policy_to_cancel.farmers:
            policy_to_cancel.farmers.remove(user)
            db.session.commit()
        # policy_recs = Policy.query.all()
        # return jsonify([{**policy.as_dict(),
        #                  'strike_event': policy.strike_event[0].desc,
        #                  'myPolicy': policy.my_policy(current_user.public_key)}
        #                 for policy in policy_recs]
        #                )
        return jsonify({
            "msg": "Cancelled policy",
            "class": "alert-danger"
        })


@data_bp.route('/mypolicies', methods=['POST', 'GET', 'DELETE'])
def mypolicies():
    if request.method == 'GET':
        # policy_recs = Policy.query.all()
        user = User.query.filter_by(wallet_address=current_user.public_key).first()
        user_policies = Policy.query.filter(Policy.farmers.contains(user)).all()

        return jsonify([{**policy.as_dict(),
                         'strike_event': policy.strike_event[0].desc,
                         'myPolicy': policy.my_policy(current_user.public_key),
                         'policy_blockchain_url': policy.policy_onchain(current_user.public_key),
                         'isPremiumPaid': policy.is_premium_paid(current_user.public_key) != '',
                         'premium_blockchain_url': policy.is_premium_paid(current_user.public_key)}
                        for policy in user_policies]
                       )


@data_bp.route('/paypremium', methods=['POST'])
def paypremium():
    if request.method == 'POST':
        policy_id = request.json

        policy = Policy.query.filter_by(id=int(policy_id)).first()

        policy_details_dict = {
            'policy': policy.name,
            'description': policy.description,
            'period': f'{policy.start_date} to {policy.end_date}',
            'coverage_amount': policy.coverage_amount,
            'strike_event': policy.strike_event[0].desc,
            'signature': f'Paid by {current_user.public_key}',
            'month_year': f'{datetime.datetime.now().month}-{datetime.datetime.now().year}'
        }

        success, txid = current_user.send(policy.premium, policy.receiver, json.dumps(policy_details_dict))

        if success:
            pymt_dict = {
                'farmer_id': current_user.public_key,
                'policy_id': int(policy_id),
                'month': datetime.datetime.now().month,
                'year': datetime.datetime.now().year,
                'blockchain_url': f'https://goalseeker.purestake.io/algorand/testnet/transaction/{txid}'
            }
            payment = PremiumPayments(**pymt_dict)
            db.session.add(payment)
            db.session.commit()

            return jsonify({
                "msg": "Payment success",
                "class": "alert-success",
                "balance": current_user.get_balance()
            })

    return jsonify({
        "msg": "Payment error",
        "class": "alert-danger"
    })


@data_bp.route('/farmdata', methods=['GET'])
def farmdata():
    try:
        farm = request.args['farm']
        try:
            limit = request.args['limit']
        except Exception as err:
            limit = 100
        farm_weather_data = Weather.query.filter_by(farm=farm) \
            .order_by(desc(Weather.created_at)).limit(limit) \
            .all()
        return jsonify([f.as_dict() for f in farm_weather_data])
    except Exception as err:
        return jsonify([])
