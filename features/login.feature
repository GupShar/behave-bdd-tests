# features/login.feature

Feature: Login on The Internet Herokuapp

  Background:
    Given the user opens the login page

  Scenario: Successful login with valid credentials
    When the user enters username "tomsmith" and password "SuperSecretPassword!"
    Then the user should see message "You logged into a secure area!"

  Scenario: Failed login with invalid password
    When the user enters username "tomsmith" and password "wrongpassword"
    Then the user should see message "Your password is invalid!"

  Scenario: Failed login with invalid username
    When the user enters username "wronguser" and password "SuperSecretPassword!"
    Then the user should see message "Your username is invalid!"

  Scenario Outline: Login with multiple credentials
    When the user enters username "<username>" and password "<password>"
    Then the user should see message "<message>"

    Examples:
      | username  | password               | message                        |
      | tomsmith  | SuperSecretPassword!   | You logged into a secure area! |
      | tomsmith  | badpass                | Your password is invalid!      |
      | baduser   | SuperSecretPassword!   | Your username is invalid!      |
