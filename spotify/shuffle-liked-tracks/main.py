from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing variables
client_id = os.getenv('client_id')
secret_id = os.getenv('secret_id')

print(client_id)
print(secret_id)