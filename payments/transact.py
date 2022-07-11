
import requests
from datetime import datetime
from payments.models import DarajaToken
from payments.daraja_auth import request_new_token
from decouple import config
import json


def initiate_transaction(sender, receiver, amount, message):
    token, expired = DarajaToken.get_credentials()
    print("Token before if....", token)
    if expired or token == None:
        new_token, expiry = request_new_token()
        if expired:
            updated_token = token.update_token(new_token)
            token = updated_token
        else:
            token = DarajaToken.objects.create(token=new_token)
    print("Token after if....", token)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {token.token}'

    }
    # timestamp = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    # print(timestamp)

    payload = {
        "BusinessShortCode": config("BUSINESS_SHORT_CODE"),
        "Password": config('DARAJA_PASSWORD'),
        "Timestamp": "20220710132848",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": sender.phone,
        "PartyB": config("BUSINESS_SHORT_CODE"),
        "PhoneNumber": sender.phone,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": receiver.account_number,
        "TransactionDesc": message
    }

    response = requests.request(
        'POST', config('MPESA_EXPRESS'), headers=headers, json=payload)
    print("\n", json.loads(response.text.encode('utf-8')), "\n")
    return json.loads(response.text.encode('utf-8'))
