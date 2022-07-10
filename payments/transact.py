
from cmath import exp
import requests
from payments.models import DarajaToken
from payments.daraja_auth import request_new_token
from decouple import config
import json


def initiate_transaction(sender, receiver, amount, message):
    token, expired = DarajaToken.get_credentials()
    if expired:
        new_token, expiry = request_new_token()
        updated_token = token.update_token(new_token)
        token = updated_token
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {token.token}'

    }

    payload = {
        "BusinessShortCode": config("BUSINESS_SHORT_CODE"),
        "Password": config('DARAJA_PASSWORD'),
        "Timestamp": "20220710132848",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": sender.phone,
        "PartyB": config("BUSINESS_SHORT_CODE"),
        "PhoneNumber": receiver.account_holder.phone,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "Siren Wagon",
        "TransactionDesc": message
    }

    response = requests.request(
        'POST', config('MPESA_EXPRESS'), headers=headers, json=payload)
    print("\n", json.loads(response.text.encode('utf-8')), "\n")
    return json.loads(response.text.encode('utf-8'))
