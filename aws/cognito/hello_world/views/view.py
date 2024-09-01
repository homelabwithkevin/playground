from functions import utils
from views import forms

def example():
    return """
    <p>
        Example Content
    </p>
    """

def navigation():
    login = utils.create_cognito_hosted_uri()

    return f"""
    <div>
        <a href='{login}'>
            <button type="submit" class="min-w-[200px] rounded-md bg-indigo-600 px-3 py-6 text-3xl font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                Login
            </button>
        </a>
    </div>
    """

def logout():
    return f"""
    <div><a href='/logout'>Logout</a></div>
    """

def index():
    return f"""
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full">
            <div>
                {utils.load_tailwind()}
                {navigation()}
            </div>
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

def dashboard(user_info):
    return f"""
        {utils.load_tailwind()}
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full text-center text-2xl">
            <div>
                <div class="mt-4">
                    <div>
                        {logout()}
                        <p>Dashboard</p>
                        <p>
                            <p>
                                Welcome {user_info.get('username')}!
                            </p>
                            {forms.form_message(user_info.get('sub'))}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """
