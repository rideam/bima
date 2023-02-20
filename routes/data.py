from flask import Blueprint, session
from models import Weather, \
    PremiumPayments, \
    User, \
    Policy, \
    db
from flask import request, jsonify
from flask_login import current_user
import datetime

data_bp = Blueprint(
    'data_bp',
    __name__
)


@data_bp.route('/weather', methods=['POST', 'GET'])
def add_weather_data():
    if request.method == 'POST':
        data = request.get_json()
        weather_dict = {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "soil_moisture": data["soil_moisture"],
            "farm": data["farm"],
            "crop": data["crop"],
        }
        weather_rec = Weather(**weather_dict)
        db.session.add(weather_rec)
        db.session.commit()

        # TODO send data to blockchain
        # TODO if strike event trigger payout

        return jsonify(weather_rec.as_dict())

    elif request.method == 'GET':
        weather_recs = Weather.query.all()
        return jsonify([weather.as_dict() for weather in weather_recs])


@data_bp.route('/policies', methods=['POST', 'GET', 'DELETE'])
def policies():
    if request.method == 'GET':
        policy_recs = Policy.query.all()
        return jsonify([{**policy.as_dict(), 'strike_event': policy.strike_event[0].desc,
                         'myPolicy': policy.my_policy(current_user.public_key)} for policy in policy_recs])

    if request.method == 'POST':
        id = request.json
        policy_to_cancel = Policy.query.filter_by(id=int(id)).one()
        user = User.query.filter_by(wallet_address=current_user.public_key).first()


        # user_not_available = True
        # for farmer in policy_to_cancel.farmers:
        #     if farmer.wallet_address == user.wallet_address:
        #         user_not_available = False
        #
        # if user_not_available:
        if user not in policy_to_cancel.farmers:
            policy_to_cancel.farmers.append(user)
            db.session.commit()
        policy_recs = Policy.query.all()
        return jsonify([{**policy.as_dict(), 'strike_event': policy.strike_event[0].desc,
                         'myPolicy': policy.my_policy(current_user.public_key)} for policy in policy_recs])

    if request.method == 'DELETE':
        id = request.json
        policy_to_cancel = Policy.query.filter_by(id=int(id)).one()
        user = User.query.filter_by(wallet_address=current_user.public_key).first()

        # user_available = False
        # for farmer in policy_to_cancel.farmers:
        #     if farmer.wallet_address == user.wallet_address:
        #         user_available = True

        # if user_available:
        if user in policy_to_cancel.farmers:
            policy_to_cancel.farmers.remove(user)
            db.session.commit()
        policy_recs = Policy.query.all()
        return jsonify([{**policy.as_dict(), 'strike_event': policy.strike_event[0].desc,
                         'myPolicy': policy.my_policy(current_user.public_key)} for policy in policy_recs])


@data_bp.route('/mypolicies', methods=['POST', 'GET', 'DELETE'])
def mypolicies():
    if request.method == 'GET':
        # policy_recs = Policy.query.all()
        user = User.query.filter_by(wallet_address=current_user.public_key).first()
        user_policies = Policy.query.filter(Policy.farmers.contains(user)).all()

        return jsonify([{**policy.as_dict(),
                         'strike_event': policy.strike_event[0].desc,
                         'myPolicy': policy.my_policy(current_user.public_key),
                         'isPremiumPaid': policy.is_premium_paid(current_user.public_key) != '',
                         'blockchain_url': policy.is_premium_paid(current_user.public_key)} for policy in user_policies])


@data_bp.route('/paypremium', methods=['POST'])
def paypremium():
    if request.method == 'POST':
        policy_id = request.json

        policy = Policy.query.filter_by(id=int(policy_id)).first()
        success, txid = current_user.send(policy.premium, policy.receiver, f'Paid by {current_user.public_key}')

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
                "class": "alert-success"
            })

    return jsonify({
        "msg": "Payment error",
        "class": "alert-danger"
    })
