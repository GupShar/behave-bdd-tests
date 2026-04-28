from behave import given,when,then

@given('the user is on login page')
def step_open_page(context):
    print("Opening login page")

@when('the user enters username {username} and password {password}')
def step_enter_credentails(context,username,password):
    context.username = username
    context.password = password
    print("Entering username and password")

@then('user sees the dashboard')
def step_verify_dashboard(context):
    assert context.username == 'admin', 'Login failed'

@then('user should see {message}')
def step_verify_message(context,message):
    print("Login failed")



