import os
import boto3
from app.lib.providers.queue_provider.abstract_queue_provider import AbstractQueueProvider
from botocore.exceptions import BotoCoreError, ClientError

class SQSQueueProvider(AbstractQueueProvider):
    
    def __init__(self) -> None:
        self.queue_url = os.getenv("SQS_ENDPOINT")
        self.client = boto3.client(
            'sqs', 
            region_name='us-east-1', 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), 
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def publish(self, message_body: str, message_attributes={}):
        try:
            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
            print(f"Mensagem enviada com sucesso. ID da mensagem: {response['MessageId']}")
            return response
        except (BotoCoreError, ClientError) as error:
            print(f"Erro ao enviar mensagem: {error}")
            return None