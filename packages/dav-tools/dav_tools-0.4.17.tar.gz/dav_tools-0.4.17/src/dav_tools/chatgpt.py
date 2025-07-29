'''Manage messages and generate answers using ChatGPT API'''

from .messages import TextFormat as _TextFormat
from .messages import message as _message, error as _error
from openai import OpenAI as _OpenAI
import os as _os
import pydantic as _pydantic


if _os.getenv('OPENAI_API_KEY') is None:
    _client = None
else:
    _client = _OpenAI()


class MessageRole:
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

class AIModel:
    GPT3 = 'gpt-3.5-turbo'
    GPT4o_mini = 'gpt-4o-mini'
    GPT4o = 'gpt-4o'

class Message:
    def __init__(self) -> None:
        self.messages = []
        self.usage = []

    def add_message(self, role: str, message):
        self.messages.append({
            'role': role,
            'content': message
        })

    def generate_answer(self, *, model=AIModel.GPT4o_mini, json_format: _pydantic.BaseModel | None = None, add_to_messages=True, **kwargs) -> str | _pydantic.BaseModel:
        """
        Generates a response based on the current conversation context.

        Args:
            model (AIModel, optional): The AI model used to generate the response. Defaults to `AIModel.GPT4o_mini`.
            json_format (_pydantic.BaseModel, optional): If provided, returns the response in the specified structured format. If `None`, the response is returned as plain text. Defaults to `None`.
            add_to_messages (bool, optional): If `True`, appends the generated response to the conversation history (`self.messages`). Defaults to `True`.
            **kwargs: Additional arguments to pass to the API.

        Returns:
            str | _pydantic.BaseModel: The generated response as plain text (`str`) or as format specified by `json_format`.

        """

        if _client is None:
            _error('You must set `OPENAI_API_KEY` in environment.')
            raise Exception('OPENAI_API_KEY not set')

        completion = _client.beta.chat.completions.parse(
            model=model,
            messages=self.messages,
            response_format={ 'type': 'text' } if json_format is None else json_format,
            **kwargs
        )

        self.usage.append(completion.usage)

        if json_format is None:
            answer = completion.choices[0].message.content
        else:
            answer = completion.choices[0].message.parsed
    
        # Add the answer to this conversation
        if add_to_messages:
            self.add_message('assistant', answer)

        return answer
    


    def print(self):
        for message in self.messages:
            role = message['role']
            if role == 'system':
                color = _TextFormat.Color.RED
            elif role == 'assistant':
                color = _TextFormat.Color.YELLOW
            else:
                color = _TextFormat.Color.BLUE

            _message(
                message['content'],
                icon=message['role'],
                icon_options=[color],
                default_text_options=[
                    color,
                    None if message['role'] == 'user' else _TextFormat.Style.ITALIC
                ]
            )

def print_price(*usage, cost_in_per_million_tokens, cost_out_per_million_tokens):
    cost_in = 0
    cost_out = 0
    
    for usage in usage:
        cost_in += usage.prompt_tokens / 1_000_000 * cost_in_per_million_tokens
        cost_out += usage.completion_tokens / 1_000_000 * cost_out_per_million_tokens

    _message(f'Cost: {(cost_in + cost_out):.5f} $ (in={usage.prompt_tokens}, out={usage.completion_tokens})',
                     icon='$', icon_options=[_TextFormat.Color.BLUE])

