# features/environment.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    """Launch browser before each scenario."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # uncomment to run without opening browser

    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    context.driver.implicitly_wait(10)
    print(f"\n>> Browser launched for: {scenario.name}")

def after_scenario(context, scenario):
    """Close browser after each scenario."""
    context.driver.quit()
    print(f"<< Browser closed for: {scenario.name}")