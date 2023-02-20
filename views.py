import json
from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, logout_user, current_user
import settings

from forms import PayForm, EnrolForm
from models import Policy, Payout

main_bp = Blueprint(
    'main_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/')
@login_required
def index():
    """Home page to display account details"""
    balance = current_user.get_balance()

    current_user.wallet_address = current_user.public_key
    # user_policies = Policy.query.filter(Policy.farmers.contains(current_user)).all()
    return render_template('index.html',
                           balance=balance,
                           address=current_user.public_key
                           )


@main_bp.route('/enrol', methods=['GET', 'POST'])
@login_required
def enrol():
    """Joining form for policy enrollment"""
    # form = EnrolForm()
    # if form.validate_on_submit():
    #     policy = {
    #         "start": "01/01/2023",
    #         "end": "30/12/2023",
    #         "description": "Cover Maize Crop, 100 hectare, to be paid 1 Algo",
    #         "Strike Event": "Temperature: 45 C, Humidity 10 %, Soil Moisture 2%",
    #         "signature": f"{form.signature.data}"
    #     }
    #     success, txid = current_user.send(0, settings.account_one_address, json.dumps(policy))
    #     return render_template('success.html', success=success, txid=txid)

    # policies = Policy.query.all()
    # policies = [policy.as_dict() for policy in policy_recs]
    return render_template('enrol.html',
                           # form=form,
                           # policies=policies,
                           signature=f"Signed by {current_user.public_key}")


# @main_bp.route('/pay', methods=['GET', 'POST'])
# @login_required
# def pay():
#     """Payment form for transactions"""
#     form = PayForm()
#     if form.validate_on_submit():
#         success, txid = current_user.send(form.amount.data, form.receiver.data, form.note.data)
#         return render_template('success.html', success=success, txid=txid)
#
#     return render_template('pay.html', form=form,
#                            receiver=settings.account_one_address,
#                            amount=0.1,
#                            note=f"Paid by {current_user.public_key}")


@main_bp.route('/payouts', methods=['GET', 'POST'])
@login_required
def payouts():
    """Payouts received"""

    pay_outs = Payout.query.filter_by(farmer_id=current_user.public_key).all()
    return render_template('payouts.html',
                           payouts=[p.as_dict() for p in pay_outs])


@main_bp.route('/mnemonic')
@login_required
def mnemonic():
    """Displays the recovery passphrase"""
    passphrase = current_user.passphrase
    return render_template('mnemonic.html', passphrase=passphrase)


@main_bp.route('/logout')
@login_required
def logout():
    """User log-out logic"""
    logout_user()
    return redirect(url_for('auth_bp.login'))
