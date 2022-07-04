from asyncore import read
from accounts.models import User
from sirenapp.models import Ambulance, Doctor, Driver, Hospital, Review, Transaction, Trip
from rest_framework import serializers


class AppUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users-detail')

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'sender',
            'account',
            'amount',
            'completed',
            'transaction_type',
            'transaction_date',
        ]

    def get_sender(self, obj):
        sender = {
            "id": obj.sender.id,
            "username": obj.sender.username,
            "account": obj.sender.account.account_number
        }
        return sender

    def get_account(self, obj):
        account = {
            "id": obj.account.id,
            "account": obj.account.account_number
        }
        if obj.account.account_holder:
            account['username'] = obj.account.account_holder.username
        else:
            account['name'] = obj.account.hospital.name

        return account

