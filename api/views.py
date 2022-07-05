import datetime
import jwt
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from sirenapp.models import CustomerAccount, Hospital, Transaction, Trip, Review, Doctor, Ambulance, Driver
from accounts.models import User
from api.serializers import UserSerializer, HospitalSerializer, ReviewSerializer, TransactionSerializer, TripSerializer, DoctorSerializer, AmbulanceSerializer, DriverSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework import serializers


# class UserViewset(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


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


class AmbulanceViewset(viewsets.ModelViewSet):
    serializer_class = AmbulanceSerializer
    queryset = Ambulance.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class DoctorViewset(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class DriverViewset(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response
