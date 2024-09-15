from datetime import datetime

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

