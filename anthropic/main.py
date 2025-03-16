import os
import anthropic

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
default_model = 'claude-3-5-haiku-20241022'

client = anthropic.Anthropic(
    api_key=api_key
)

def get_tokens(use_model, content):
    response = client.messages.count_tokens(
        model=use_model,
        messages=[
            {"role": "user", "content": content}
        ]
    )
    print(response)


def list_models():
    models = client.models.list(limit=20)

    for model in models:
        print(model.id)


def message(content, max_tokens=1024):
    response = client.messages.create(
        model=default_model,
        max_tokens=max_tokens, # 8192 max
        messages=[
            {"role": "user", "content": content}
        ]
    )
    input_tokens = response.usage.input_tokens
    cost_input_tokens = (input_tokens / 1000000) * .8
    output_tokens = response.usage.output_tokens
    cost_output_tokens = (input_tokens / 1000000) * .4

    result = response.content
    print(f'Input: {input_tokens} - {cost_input_tokens}')
    print(f'Output {output_tokens} - {cost_output_tokens}')
    print(f'Raw Response: {response}')
    print(f'\nResult:')

    for r in result:
        print(r.text)

file = open('main.py').read()

content = "Can you please refactor this code? It's written in python. \n\n"
content += file
get_tokens(default_model, content)
message(content, 8192) # 8192 max tokens