@negative
Feature: Empty Search Result Handling

  Background:
    Given I open the Nykaa Baby Care page

  @no_results
  Scenario: Validate the page handles empty product scenarios
    When I open the Nykaa Baby Care page with a forced empty query
    Then the page should not crash and should display a response
