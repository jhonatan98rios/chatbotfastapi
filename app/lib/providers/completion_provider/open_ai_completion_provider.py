import os
import json
from typing import List
from app.lib.entities.completion import Completion
from app.lib.errors.internal_server_error import InternalServerErrorException
from app.lib.providers.completion_provider.abstract_completion_provider import AbstractCompletionProvider
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai import OpenAI

class OpenAiCompletionProvider(AbstractCompletionProvider):
    
    __slots__ = ['client']

    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    def execute(self, instructions: str, footer: str, messages: List[ChatCompletionMessageParam]) -> Completion:
        
        # instructions = """
        #     Se comporte como um chatbot em uma API Rest e responda as perguntas enviadas a seguir exclusivamente como um json no formato { answer: str }. Seja educado e de espaço para o cliente dizer o que precisa sem ser muito direto para não soar rude. Se ele estiver interessado em comprar, descubra qual o produto, marca, modelo e quantidade que o usuario deseja. Caso o usuario deseje seguir com a compra, solicite os dados pessoais como nome, email e endereço. Apos ter esses dados, adicione os dados para abertura de ordem de serviço { name: str, mail: str, address: str, product: str, quantity: int } na resposta. Somente adicione os campos caso o usuário deixe claro o interesse em realizar a compra e também forneça todos os dados, sem falta. Tenha certeza de que todos os dados foram fornecidos. Cuidado para não autopreencher os dados do usuário, como nome, email e endereço. Ao final da compra, envie como resposta uma confirmação da solicitação de compra e avise que um email com o boleto será enviado para o email do cliente.
        # """
        
        # # Caso o usuario demonstre interesse em algum produto mas demonstre que nao ira finalizar a compra no momento, adicione o campo { followup: int }, que servira para fazer remarketing e o follow-up daquele usuario. O campo followup deve trazer o valor em dias para voltarmos a entrar em contato. Somente adicione o campo followup, caso haja a possibilidade da conclusao da compra, ou nao fique explicito a desistencia da conclusao da compra.
        # footer = "Somente responda as mensagens agindo como uma API Rest e utilizando a estrutura json { answer: str, name: str, mail: str, address: str, product: str, quantity: int } como resposta. A resposta não deve conter os parametros com valor null."

        
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instructions},
                *messages,
                {"role": "system", "content": footer},
            ]
        )
        
        content = completion.choices[0].message.content
        
        if content is None:
            raise InternalServerErrorException(detail="Erro ao se comunicar com a API da Open AI")
        
        completion = Completion(**json.loads(content))
        
        print(completion)
        return completion
    