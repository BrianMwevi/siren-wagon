from rest_framework import serializers
from rest_framework import viewsets, generics

from api.serializers import AppUserSerializer, HospitalSerializer, ReviewSerializer, TransactionSerializer, TripSerializer, DoctorSerializer, AmbulanceSerializer, DriverSerializer
from accounts.models import User
from sirenapp.models import CustomerAccount, Hospital, Transaction, Trip, Review, Doctor, Ambulance, Driver

from django.db.models import Q


class AppUserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AppUserSerializer


class TransactionsView(generics.ListCreateAPIView):
    """The view class for creating and retrieving transactions only. One can't edit/change an existing transaction."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """The method gets all the transactions associated with the current authenticated user. It returns a list of sent and/or received transactions."""
        account = self.request.user.customer_account.first()
        transactions = Transaction.objects.filter(
            Q(sender=self.request.user) | Q(account=account))
        return transactions

    def perform_create(self, serializer):
        """Method to create a new transaction. Checks if the sender has sufficient balance before transacting and raises an exception if the balance is less the amount to be transacted."""

        receiver_account_number = self.request.data['account_number']
        sender = self.request.user.customer_account.first()
        transaction_type = self.request.data['transaction_type'].lower()

        can_transact = CustomerAccount.can_transact(
            sender.account_number, self.request.data['amount'])

        if can_transact or (transaction_type == "deposit" and receiver_account_number == sender.account_number):
            account = CustomerAccount.get_account(receiver_account_number)
            serializer.save(sender=self.request.user, account=account)
        else:
            raise serializers.ValidationError(
                {"detail": "You have insufficient account balance"})


class HospitalViewset(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()


class TripViewset(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

