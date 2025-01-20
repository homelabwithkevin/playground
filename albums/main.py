import os
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")
print(base_path)