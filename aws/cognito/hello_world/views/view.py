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

def dashboard(request_headers):
    parse_request_headers = utils.parse_request_headers(request_headers)
    return f"""
        <div class="text-center mt-4">
            {utils.load_tailwind()}
            <p>Dashboard</p>
            <p>
                <p>Request Headers</p>
                <p>
                    {parse_request_headers}
                </p>
            </p>
        </div>
    """
