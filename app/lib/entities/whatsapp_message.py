from pydantic import BaseModel
from typing import Optional

class WhatsappMessage(BaseModel):
    # Refatorar de acordo com o retorno do Twilio
    SmsMessageSid: str
    NumMedia: str
    ProfileName: Optional[str]
    WaId: str
    Body: Optional[str]
    From: str
    To: str
    MessageSid: str
    AccountSid: str
    NumSegments: Optional[str]
    SmsStatus: str
    MediaUrl0: Optional[str] = None
    MediaContentType0: Optional[str] = None