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
    <div class="grid grid-cols-3">
        <div><a href='{login}'>Login</a></div>
    </div>
    """

def index():
    return f"""
        <div class="text-center mt-4">
            {utils.load_tailwind()}
            {navigation()}
        </div>
    """

def callback(code=None):
    return f"""
        <div class="text-center mt-4">
            {utils.load_tailwind()}
            <p>Callback</p>
            <p>Code: {code}</p>
        </div>
    """

def dashboard():
    return f"""
        <div class="text-center mt-4">
            {utils.load_tailwind()}
            <p>Dashboard</p>
        </div>
    """
