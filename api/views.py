from rest_framework.response import Response
from rest_framework import serializers, viewsets, generics, views
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken


from django.db.models import Q

from sirenapp.models import CustomerAccount, Hospital, Package, Transaction, Trip, Review, Doctor, Ambulance, Driver
from accounts.models import User, PatientProfile, EmergencyContact
from api.serializers import EmergencyContactSerializer, PackageSerializer, HospitalSerializer, ReviewSerializer, TransactionSerializer, TripSerializer, DoctorSerializer, AmbulanceSerializer, DriverSerializer, PatientProfileSerializer, UserSerializer
from payments.transact import initiate_transaction


class UserRegisterView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class EmergencyContactViewset(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    queryset = EmergencyContact.objects.all()

    def get_queryset(self):
        contacts = EmergencyContact.objects.filter(patient=self.request.user)
        return contacts

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class PatientProfileView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewset(viewsets.ModelViewSet):
    """The view class for creating and retrieving transactions only. One can't edit/change an existing transaction."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """The method gets all the transactions associated with the current authenticated user. It returns a list of sent and/or received transactions."""
        receiver = self.request.user.customer_account.first()
        transactions = Transaction.objects.filter(
            Q(sender=self.request.user) | Q(receiver=receiver))
        return transactions

    def perform_create(self, serializer):
        """Method to create a new transaction. Checks if the sender has sufficient balance before transacting and raises an exception if the balance is less the amount to be transacted."""
        sender = self.request.user
        receiver = CustomerAccount.objects.get(
            account_number=self.request.data['receiver'])
        message = self.request.data['transaction_type'].lower()
        if sender.customer_account.first().account_number == receiver.account_number and message == 'transfer':
            raise serializers.ValidationError(
                {"detail": "Did you mean to deposit? You can't send money to yourself"})
        amount = self.request.data['amount']
        response = initiate_transaction(
            sender, receiver, amount, message)

        if "errorMessage" in response:
            raise serializers.ValidationError(
                {'detail': response['errorMessage']})
        serializer.save(sender=sender, receiver=receiver)


class SuccessfulPayments(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # def perform_create


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


class PackageViewset(viewsets.ModelViewSet):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class PaymentView(generics.CreateAPIView):
#     serializer_class = TransactionSerializer
#     queryset = Transaction.objects.all()

#     def perform_create(self, serializer):
#         sender = self.request.user
#         receiver = CustomerAccount.objects.get(
#             account_holder__id=self.request.data['receiver'])
#         amount = self.request.data['amount']
#         message = self.request.data['transaction_type']
#         response = initiate_transaction(
#             sender, receiver, amount, message)
#         try:

#             error_message = response['errorMessage']
#             raise serializers.ValidationError(
#                 {'detail': error_message})
#         except:
#             serializer.save(sender=sender, receiver=receiver)
