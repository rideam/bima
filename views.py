from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user
import settings
from sqlalchemy import desc
from models import Policy, Payout, Weather

main_bp = Blueprint(
    'main_bp',
    __name__,
    template_folder=f'templates/{settings.template_mode}',
    static_folder='static'
)


@main_bp.route('/')
@login_required
def index():
    """Home page to display account details"""
    balance = current_user.get_balance()

    current_user.wallet_address = current_user.public_key
    return render_template(
        'index.html',
        balance=balance,
        address=current_user.public_key
    )


@main_bp.route('/enrol', methods=['GET', 'POST'])
@login_required
def enrol():
    """Joining a policy"""

    return render_template(
        'enrol.html',
        signature=f"Signed by {current_user.public_key}"
    )


@main_bp.route('/payouts', methods=['GET', 'POST'])
@login_required
def payouts():
    """Payouts received"""

    pay_outs = Payout.query.filter_by(farmer_id=current_user.public_key) \
        .join(Policy, Policy.id == Payout.policy_id) \
        .add_columns(Policy.name) \
        .all()
    p = [{**p[0].as_dict(), 'name': p[1]} for p in pay_outs]
    return render_template('payouts.html', payouts=p)


@main_bp.route('/sensordata', methods=['GET', 'POST'])
@login_required
def sensordata():
    """Payment form for transactions"""

    farm_weather_data = Weather.query.filter_by(user=current_user.public_key) \
        .order_by(desc(Weather.created_at)).limit(100) \
        .all()
    return render_template(
        'sensordata.html',
        farm_weather_data=[f.as_dict() for f in farm_weather_data]
    )


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
