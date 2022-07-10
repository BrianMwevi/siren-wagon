<<<<<<< HEAD

import requests
from decouple import config
import base64
from datetime import datetime

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {config("DARAJA_TOKEN")}'
}


def transaction_payload(sender, receiver, amount, transaction_type):
    passkey = config('PASS_KEY'),
    timestamp = datetime.now().strftime("%Y%M%d%H%M%S")
    shortcode = config("BUSINESS_SHORT_CODE")

    payload = {
        "BusinessShortCode": shortcode,
        "Timestamp": datetime.now().strftime("%Y%M%d%H%M%S"),
        "PassKey": passkey,
        "Password": base64.encode(shortcode+passkey+timestamp),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": sender.phone,  # phone number
        "PartyB": config("PARTY_B"),  # paybill number
        "PhoneNumber": receiver.phone,  # phone number
        "CallBackURL": config("CALLBACK_URL"),
        "AccountReference": config("ACCOUNT_REFERENCE"),
        "TransactionDesc": transaction_type,
    }

    response = requests.request(
        "POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, data=payload)
    print(response.text.encode('utf8'))
=======
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
        print("New token: ", new_token, expiry)
        updated_token = token.update_token(new_token)
        token = updated_token
    headers = {
        # 'Content-Type': 'application/json',
        # 'Authorization': f'Bearer {token.token}'
        'Authorization': 'Bearer tLWhI7aGRBrXZjdkhmHV6ZCUcipx'

    }

    payload={
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwNzEwMjMwNzEy",
        "Timestamp": "20220710230712",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708374149,
        "PartyB": 600000,
        "PhoneNumber": 254708374149,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }
    # {
    #     "BusinessShortCode": 174379,
    #     "Password": config("DARAJA_PASSWORD"),
    #     "Timestamp": "20220710132848",
    #     "TransactionType": "CustomerPayBillOnline",
    #     "Amount": amount,
    #     "PartyA": sender.phone,
    #     "PartyB": 174379,
    #     "PhoneNumber": receiver.account_holder.phone,
    #     "CallBackURL": "https://mydomain.com/path",
    #     "AccountReference": "Siren Wagon",
    #     "TransactionDesc": message
    # }

    response = requests.request(
        'POST', config('MPESA_EXPRESS'), headers=headers, data=payload)
    print(response.text.encode('utf-8'))
    return json.loads(response.text.encode('utf-8'))
>>>>>>> develop
