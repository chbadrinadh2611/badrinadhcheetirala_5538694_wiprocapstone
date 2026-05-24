@positive
Feature: Product Page Validation on Nykaa

  Background:
    Given I open the Nykaa Baby Care page

  @validation @smoke
  Scenario: Validate product cards are displayed
    Then products should be displayed on the page

  @validation
  Scenario: Validate current URL contains baby-care
    Then the URL should contain "baby-care"

  @validation
  Scenario: Validate page title is not empty
    Then the page title should not be empty

  @validation
  Scenario: Validate product count is greater than zero
    Then the product count should be greater than 0
