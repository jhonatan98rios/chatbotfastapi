import os
import json
from app.lib.entities.completion import Completion
from app.lib.errors.internal_server_error import InternalServerErrorException
from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider
from openai import OpenAI

class OpenAiCompletionProvider(AbstractCompletionProvider):
    
    __slots__ = ['client', 'instructions']

    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.instructions = """
            Se comporte como um chatbot em uma API Rest e responda as perguntas enviadas a seguir como um json no formato { answer: str }. Alem da resposta, preciso que voce me envie um resumo das perguntas e repostas enviadas ate o momento. Simplifique ao maximo as perguntas e respostas e envie elas em uma outra chave no seguinte formato: { answer: str, context: str }. Caso o usuario solicite uma compra, adicione uma estrutura semelhante a essa com os dados para abertura de ordem de serviço { answer: str, context: str, product: str, quantity: int }. Caso o usuario demonstre interesse em algum produto mas demonstre que nao ira finalizar a compra no momento, adicione o campo { followup: int }, que servira para fazer remarketing e o follow-up daquele usuario. O campo followup deve trazer o valor em dias para voltarmos a entrar em contato. So adicione o campo followup, caso haja a possibilidade da conclusao da compra, ou nao fique explicito a desistencia da conclusao da compra.
        """


    def execute(self, message: str) -> Completion:
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": message}
            ]
        )
        
        content = completion.choices[0].message.content
        
        if content is None:
            raise InternalServerErrorException(detail="Erro ao se comunicar com a API da Open AI")
        
        completion = Completion(**json.loads(content))
        
        print(completion)
        return completion
    