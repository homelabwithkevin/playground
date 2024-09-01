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
    <div><a href='{login}'>Login</a></div>
    """

def logout():
    return f"""
    <div><a href='/Prod/logout'>Logout</a></div>
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

def dashboard(request_headers):
    parse_request_headers = utils.parse_request_headers(request_headers)
    access_token = parse_request_headers['access_token']

    if access_token: 
        sub, email_verified, email, username = utils.get_user_info(access_token)

    return f"""
        <div class="text-center mt-4">
            {utils.load_tailwind()}
            {logout()}
            <p>Dashboard</p>
            <p>
                <p>
                    Welcome {email}
                </p>
            </p>
        </div>
    """
