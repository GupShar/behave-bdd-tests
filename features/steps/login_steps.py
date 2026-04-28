# features/steps/login_steps.py

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://the-internet.herokuapp.com"


@given('the user opens the login page')
def step_open_login_page(context):
    context.driver.get(f"{BASE_URL}/login")
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "login"))
    )
    print("  -> Login page loaded")


@when('the user enters username "{username}" and password "{password}"')
def step_enter_credentials(context, username, password):
    user_field = context.driver.find_element(By.ID, "username")
    user_field.clear()
    user_field.send_keys(username)

    pass_field = context.driver.find_element(By.ID, "password")
    pass_field.clear()
    pass_field.send_keys(password)

    context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print(f"  -> Submitted: {username} / {password}")


@then('the user should see message "{expected_message}"')
def step_verify_flash_message(context, expected_message):
    # Wait for the flash div to appear
    flash_element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash"))
    )

    # FIX: The flash div contains a close button (×) as a child <a> tag.
    # flash_element.text includes "×" — so we use JavaScript to get
    # only the direct text node, excluding child elements.
    actual_message = context.driver.execute_script(
        """
        var el = arguments[0];
        var text = '';
        for (var i = 0; i < el.childNodes.length; i++) {
            if (el.childNodes[i].nodeType === 3) {   // Node.TEXT_NODE = 3
                text += el.childNodes[i].textContent;
            }
        }
        return text.trim();
        """,
        flash_element
    )

    assert expected_message in actual_message, (
        f"\n  Expected : '{expected_message}'"
        f"\n  Actual   : '{actual_message}'"
    )
    print(f"  -> ✅ Verified: '{actual_message}'")
