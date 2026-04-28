Feature: Login to the internet app

  Background:the user is on login page
    Given the user is on login page


  Scenario: Successful login
    When the user enters username "admin" and password "admon123"
    Then user sees the dashboard

  Scenario: Invalid Username
    When the user enters username "admin" and password "admin13"
    Then user should see "Invalid credentials"

  Scenario Outline: Login with multiple users
    When the user enters username {username} and password {password}
    Then user sees the dashboard

    Examples:
    |username|password|
    |admin   |admin123|
    |admin   |admin12 |


