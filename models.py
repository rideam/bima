from algosdk import mnemonic
from algosdk.account import address_from_private_key
from flask_login import UserMixin

from algod import get_balance, send_txn
from indexer import get_transactions


class User(UserMixin):
    """User account model"""

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

    def get_transactions(self, substring):
        """Returns a list of the user's transactions"""
        return get_transactions(self.public_key, substring)
