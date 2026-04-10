import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("TWILIO_TOKEN")

FROM_WHATSAPP = "whatsapp:+14155238886"

TO_WHATSAPP_LIST = [
    "whatsapp:+91XXXXXXXXXX"
]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_alert(message):
    if not ACCOUNT_SID or not AUTH_TOKEN:
        print("Missing credentials")
        return

    for number in TO_WHATSAPP_LIST:
        try:
            client.messages.create(
                body=message,
                from_=FROM_WHATSAPP,
                to=number
            )
        except Exception as e:
            print(e)