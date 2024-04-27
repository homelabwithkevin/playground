
import os

def load_env():
    if not os.path.exists(".env"):
        print("No env file!")
        return

    print("Loading .env file...")
    config = open(".env", "r")

    for line in config:
        key, value = line.strip().split("=")
        os.environ[key] = value

    return os.environ['pictures']


picture_path = load_env()

for root, dirs, files in os.walk(picture_path):
    for file in files:
        print(''.join([root, '\\', file]))