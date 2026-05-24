@negative
Feature: Invalid Filter Handling

  Background:
    Given I open the Nykaa Baby Care page

  @invalid_filter
  Scenario: Apply an unavailable filter combination returns graceful response
    When I expand the Brand filter
    And I select the brand "Mamaearth"
    And I expand the Avg Customer Rating filter
    And I select the rating "4 Stars & Above"
    Then the page should handle the filter gracefully
