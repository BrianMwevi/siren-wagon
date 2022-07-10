
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
