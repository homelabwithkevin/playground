from functions import utils, db
from views import forms

def example():
    return """
    <p>
        Example Content
    </p>
    """

def view_login():
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
    <div class="m-4">
        <a href='/logout'>Logout</a>
    </div>
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
    is_password_set = False
    users_password = user_info.get('password')
    if users_password:
        is_password_set = True

    return f"""
        {utils.load_tailwind()}
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full text-center text-2xl">
            <div>
                <div class="mt-4">
                    <div class="space-y-4">
                        {logout()}
                        {header()}
                        <p>
                            <p>
                                Welcome {user_info.get('given_name')}!
                            </p>
                            <p>
                                Current Password: {is_password_set}
                            </p>
                            {forms.form_message(user_info.get('sub'))}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """

def parse_post_details(post_details):
    data = f"""
    <table class="table-fixed">
        <thead>
            <tr>
                <th>Date</th>
                <th>Message</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{post_details['date']['S']}</td>
                <td>{post_details['message']['S']}</td>
            </tr>
        </tbody>
    </table>
    """
    return data

def post(path, user_info):
    result_path = path.split('/post/')[1]
    result_post_details = None
    parsed_details = None

    try:
        result_post_details = db.get_item(result_path, user_info)
        parsed_details = parse_post_details(result_post_details)
    except Exception as e:
        print(f'Failed to get item: {e}')

    return f"""
        {utils.load_tailwind()}
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full text-center text-2xl">
            <div>
                <div class="mt-4">
                    <div>
                        {logout()}
                        <div class="mt-4">Post by {user_info.get('username')}</div>
                        <div class="mt-4"> {parsed_details} </div>
                    </div>
                </div>
            </div>
        </div>
    """

def view_journal(user_info):
    is_password_set = False
    users_password = user_info.get('password')
    if users_password:
        is_password_set = True

    return f"""
        {utils.load_tailwind()}
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full text-center text-2xl">
            <div>
                <div class="mt-4">
                    <div class="space-y-4">
                        {logout()}
                        {header()}
                        <div>Password: {is_password_set}</div>
                        <div>Today: {utils.today_journal()}</div>
                        <p>
                            <p>
                                Welcome {user_info.get('given_name')}!
                            </p>
                            {forms.form_message(user_info.get('sub'), 'journal', users_password)}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """

def view_password(user_info):
    is_password_set = False
    users_password = user_info.get('password')
    if users_password:
        is_password_set = True
    return f"""
        {utils.load_tailwind()}
        <div class="flex justify-center mt-8 max-w-[400px] lg:max-w-full text-center text-2xl">
            <div>
                <div class="mt-4">
                    <div class="space-y-4">
                        {logout()}
                        {header()}
                        <div>Set a Password for Encryption</div>
                        <div>
                            Current Password: {is_password_set}
                        </div>
                        <p>
                            {forms.form_message(user_info.get('sub'), 'password')}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """

def header():
    return f"""
        <div><a href="/dashboard">Dashboard</a></div>
        <div><a href="/password">Password</a></div>
        <div><a href="/journal">Journal</a></div>
    """