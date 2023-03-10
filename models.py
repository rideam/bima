from algosdk import mnemonic
from algosdk.account import address_from_private_key
from flask_login import UserMixin
from algod import get_balance, send_txn

from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class Farm(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    """User account model"""

    wallet_address = db.Column(db.String(255), primary_key=True)
    roles = db.relationship('Role', secondary="roles_users",
                            backref=db.backref('users', lazy='dynamic'))
    farms = db.relationship('Farm', secondary="farms_users",
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, passphrase):
        """Creates a user using the 25-word mnemonic"""
        self.passphrase = passphrase

    @property
    def id(self):
        """Returns private key from mnemonic"""
        return mnemonic.to_private_key(self.passphrase)

    @property
    def public_key(self):
        """Returns user's address"""
        return address_from_private_key(mnemonic.to_private_key(self.passphrase))

    def get_balance(self):
        """Returns user balance, in algos"""
        return get_balance(self.public_key)

    def send(self, quantity, receiver, note):
        """Returns True and Transaction id for a successful transaction. Quantity is given in algos"""
        return send_txn(self.public_key, quantity, receiver, note, self.id)

    def __eq__(self, other):
        return self.wallet_address == other.wallet_address


class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    soil_moisture = db.Column(db.Float, nullable=False)
    farm = db.Column(db.String(255), nullable=False)
    crop = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(255), nullable=True)
    blockchain_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return '<Weather %r>' % (self.id)

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for c in self.__table__.columns:
            if isinstance(c.type, db.DateTime) and getattr(self, c.name) is not None:
                result[c.name] = getattr(self, c.name).strftime('%d-%m-%Y %H:%M')
        return result


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    temperature_condition = db.Column(db.String(100),
                                      nullable=True)
    humidity = db.Column(db.Float, nullable=False)
    humidity_condition = db.Column(db.String(100), nullable=True)
    soil_moisture = db.Column(db.Float, nullable=False)
    soil_moisture_condition = db.Column(db.String(100), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        return self.name

    @property
    def desc(self):
        return f'Temp {self.temperature_condition} {self.temperature} C; ' \
               f'Humidity {self.humidity_condition} {self.humidity}%; ' \
               f'Moisture {self.soil_moisture_condition} {self.soil_moisture} %'


class PremiumPayments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    farmer_id = db.Column(db.String(255), db.ForeignKey('user.wallet_address'))
    policy_id = db.Column(db.Integer(), db.ForeignKey('policy.id'))
    month = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    blockchain_url = db.Column(db.Text)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Payout(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    farmer_id = db.Column(db.String(255), db.ForeignKey('user.wallet_address'))
    policy_id = db.Column(db.Integer(), db.ForeignKey('policy.id'))
    amount = db.Column(db.Float(), nullable=False)
    payout_date = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())
    blockchain_url = db.Column(db.String(255))

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for c in self.__table__.columns:
            if isinstance(c.type, db.DateTime) and getattr(self, c.name) is not None:
                result[c.name] = getattr(self, c.name).strftime('%d-%m-%Y %H:%M')
        return result


class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    premium = db.Column(db.Float, nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    receiver = db.Column(db.String(255))  # nullable=False
    strike_event = db.relationship('Event', secondary="policies_events", post_update=True,
                                   backref=db.backref('policies', lazy='dynamic'))
    farmers = db.relationship('User', secondary="policies_users", post_update=True,
                              backref=db.backref('policies', lazy='dynamic'))

    def as_dict(self):
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for c in self.__table__.columns:
            if isinstance(c.type, db.Date) and getattr(self, c.name) is not None:
                result[c.name] = getattr(self, c.name).strftime('%d-%m-%Y')
        return result

    def is_valid(self, date, farmer_id):
        return self.start_date <= date <= self.end_date and self.is_premium_paid(farmer_id)

    def my_policy(self, address):
        result = False
        for f in self.farmers:
            if f.wallet_address == address:
                result = True
        return result

    def is_premium_paid(self, farmer_id):
        is_paid = PremiumPayments.query.filter_by(farmer_id=farmer_id,
                                                  policy_id=self.id,
                                                  month=datetime.datetime.now().month,
                                                  year=datetime.datetime.now().year).first()
        if is_paid:
            return is_paid.blockchain_url
        return ''

    def policy_onchain(self, farmer_id):
        policy_farmer_rec = PoliciesFarmers.query.filter_by(farmer_id=farmer_id,
                                                            policy_id=self.id).first()
        if policy_farmer_rec.blockchain_url:
            return policy_farmer_rec.blockchain_url
        return ''

    def __str__(self):
        return self.name


class PoliciesEvents(db.Model):
    __tablename__ = "policies_events"

    id = db.Column(db.Integer(), primary_key=True)
    policy_id = db.Column(db.Integer(), db.ForeignKey('policy.id', ondelete='CASCADE'))
    event_id = db.Column(db.Integer(), db.ForeignKey('event.id', ondelete='CASCADE'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PoliciesFarmers(db.Model):
    __tablename__ = "policies_users"

    id = db.Column(db.Integer(), primary_key=True)
    policy_id = db.Column(db.Integer(), db.ForeignKey('policy.id', ondelete='CASCADE'))
    farmer_id = db.Column(db.String(255), db.ForeignKey('user.wallet_address', ondelete='CASCADE'))
    blockchain_url = db.Column(db.String(255), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RolesUsers(db.Model):
    __tablename__ = "roles_users"

    id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
    user_wallet_address = db.Column(db.String(255), db.ForeignKey('user.wallet_address', ondelete='CASCADE'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class FarmsUsers(db.Model):
    __tablename__ = "farms_users"

    id = db.Column(db.Integer(), primary_key=True)
    farm_id = db.Column(db.Integer(), db.ForeignKey('farm.id', ondelete='CASCADE'))
    user_wallet_address = db.Column(db.String(255), db.ForeignKey('user.wallet_address', ondelete='CASCADE'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
