def random_string():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

