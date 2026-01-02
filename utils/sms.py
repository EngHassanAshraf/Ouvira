from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

def send_sms(phone: str, message: str, from_number: str) -> bool:

    try:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=phone
        )

        print(f"SMS sent to {phone}, SID: {sms.sid}")
        return True

    except TwilioRestException as e:
        print("Twilio error:", str(e))
        return False
