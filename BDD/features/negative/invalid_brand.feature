@negative
Feature: Invalid Brand Filter Handling

  Background:
    Given I open the Nykaa Baby Care page

  @invalid_brand
  Scenario: Search for a non-existent brand shows no results
    When I expand the Brand filter
    And I search for an invalid brand "XYZ_NONEXISTENT_BRAND_999"
    Then no brand results should be displayed
