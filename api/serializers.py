from asyncore import read
from requests import Response
from rest_framework import serializers
from sirenapp.models import Ambulance, Doctor, Driver, Hospital, Review, Transaction, Trip, Package
from accounts.models import EmergencyContact, PatientProfile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'], phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class PackageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='packages-detail')

    class Meta:
        model = Package
        fields = [
            'url',
            'id',
            'package_choice',
            'amount',
        ]


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyContact
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'id_number',
            'phone1',
            'phone2',
            'phone3',
            'relationship',

        ]


class PatientProfileSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='patients-detail')
    user = UserSerializer(read_only=True)
    account = serializers.SerializerMethodField()
    package = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            # 'url',
            'id',
            'user',
            'id_number',
            'picture',
            'emergency_contacts',
            'package',
            'medical_conditions',
            'picture',
            'account',
        ]

    def get_account(self, obj):
        return obj.account.account_number


class TransactionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='transactions-detail')
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'url',
            'id',
            'sender',
            'receiver',
            'amount',
            'completed',
            'transaction_type',
            'transaction_date',
        ]

    def get_sender(self, obj):
        sender = {
            "id": obj.sender.id,
            "username": obj.sender.username,
            "account_number": obj.sender.patient.account.account_number
        }
        return sender

    def get_receiver(self, obj):
        receiver = {
            "id": obj.receiver.id,
            "account_number": obj.receiver.account_number
        }
        if obj.receiver.account_holder:
            receiver['username'] = obj.receiver.account_holder.username
        else:
            receiver['name'] = obj.receiver.hospital.name

        return receiver


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='hospitals-detail')
    patients = UserSerializer(read_only=True, required=False, many=True)
    ambulances = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False, many=True)
    doctors = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False, many=True)
    reviews = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False, many=True)
    account = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Hospital
        fields = [
            'url',
            'id',
            'name',
            'location',
            'patients',
            'ambulances',
            'doctors',
            'reviews',
            'account',
            'established_date',
            'updated_date',
        ]

    def get_account(self, obj):
        return obj.account.account_number


class TripSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='trips-detail')
    fee = TransactionSerializer(read_only=True)
    destination = HospitalSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = [
            'url',
            'id',
            'pickup',
            'destination',
            'persons',
            'fee',
            'trip_date',
            'completed',
        ]


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='drivers-detail')
    trips = TripSerializer(read_only=True, many=True)

    class Meta:
        model = Driver
        fields = [
            'url',
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'trips',
        ]


class AmbulanceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ambulances-detail')
    trips = TripSerializer(read_only=True, many=True)
    ratings = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Ambulance
        fields = [
            'url',
            'id',
            'driver',
            'number_plate',
            'available',
            'trips',
            'ratings',
        ]


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    ambulance = AmbulanceSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'ambulance',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ambulance = AmbulanceSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'user',
            'hospital',
            'ambulance',
            'content',
            'rating',
            'created_date',
        ]
