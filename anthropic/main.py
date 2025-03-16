import os
import anthropic

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')


client = anthropic.Anthropic(
    api_key=api_key
)

models = client.models.list(limit=20)
for model in models:
    if not 'opus' in model.id:
        print(model.id)