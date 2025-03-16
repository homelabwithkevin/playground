import os
import logging

from typing import Optional, List

import anthropic
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnthropicAssistant:
    def __init__(self,
                 api_key: Optional[str] = None,
                 default_model: str = 'claude-3-5-haiku-20241022'):
        """
        Initialize the Anthropic Assistant

        :param api_key: Anthropic API key (defaults to environment variable)
        :param default_model: Default model to use
        """
        # Load environment variables
        load_dotenv()

        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("No API key provided. Set API_KEY in .env or pass directly.")

        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.default_model = default_model

    def count_tokens(self, content: str, model: Optional[str] = None) -> int:
        """
        Count tokens for given content

        :param content: Text to count tokens for
        :param model: Model to use (defaults to default model)
        :return: Number of tokens
        """
        try:
            model = model or self.default_model
            response = self.client.messages.count_tokens(
                model=model,
                messages=[{"role": "user", "content": content}]
            )
            return response.input_tokens
        except Exception as e:
            logger.error(f"Token counting error: {e}")
            return 0

    def list_models(self, limit: int = 20) -> List[str]:
        """
        List available models

        :param limit: Number of models to list
        :return: List of model IDs
        """
        try:
            models = self.client.models.list(limit=limit)
            return [model.id for model in models]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def generate_message(self,
                         content: str,
                         max_tokens: int = 1024,
                         model: Optional[str] = None) -> str:
        """
        Generate a message using the AI

        :param content: Prompt content
        :param max_tokens: Maximum tokens to generate
        :param model: Model to use (defaults to default model)
        :return: Generated text
        """
        try:
            model = model or self.default_model
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": content}]
            )

            # Calculate token costs
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost_input = (input_tokens / 1_000_000) * 0.8
            cost_output = (output_tokens / 1_000_000) * 0.4

            # Log token usage
            logger.info(f'Input Tokens: {input_tokens} (Cost: ${cost_input:.4f})')
            logger.info(f'Output Tokens: {output_tokens} (Cost: ${cost_output:.4f})')

            # Return first content text
            return response.content[0].text if response.content else ""

        except Exception as e:
            logger.error(f"Message generation error: {e}")
            return ""

def main():
    try:
        # Initialize assistant
        assistant = AnthropicAssistant()

        # Read the file
        # with open('main.py', 'r') as file:
        #     file_content = file.read()

        # Prepare content
        content = "Can you please refactor this code? It's written in python. \n\n"
        # content += file_content

        # Count tokens
        token_count = assistant.count_tokens(content)
        logger.info(f"Total tokens: {token_count}")

        # Generate message
        result = assistant.generate_message(content, max_tokens=8192)
        print("\nRefactored Result:")
        print(result)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()