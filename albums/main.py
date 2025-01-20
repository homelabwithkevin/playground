import os
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("BASE_PATH")

def walk_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

for file in walk_directory(base_path):
    print(file)