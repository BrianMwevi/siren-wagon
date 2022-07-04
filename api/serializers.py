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

