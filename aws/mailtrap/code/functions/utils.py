from datetime import datetime

def today():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today_newsletter():
    return datetime.now().strftime("%Y-%m-%d")

