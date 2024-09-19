import os
from twilio.rest import Client # type: ignore
from app.lib.providers.message_provider.abstract_message_provider import AbstractMessageProvider


class TwilioMessageProvider(AbstractMessageProvider):

    client: Client
    
    def __init__(self) -> None:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.client = Client(account_sid, auth_token)

    def sendMessage(self, id: str, to: str, body: str):
        self.client.messages.create(
            messaging_service_sid="MG9752274e9e519418a7406176694466fa",
            to="+15558675310",
            body="This will be the body of the new message!",
        )