from functions import utils

def example():
    return """
    <p>
        Example Content
    </p>
    """

def navigation():
    login = utils.create_cognito_hosted_uri()

    return f"""
    <ul>
        <li><a href='{login}'>Login</a></li>
        <li><a>Logout</a></li>
    </ul>
    """
