@positive
Feature: Brand Filter on Nykaa Baby Care

  Background:
    Given I open the Nykaa Baby Care page

  @brand @smoke
  Scenario Outline: Apply brand filter and validate products
    When I expand the Brand filter
    And I select the brand "<brand>"
    Then products should be displayed on the page

    Examples:
      | brand      |
      | Mamaearth  |
      | Himalaya   |
      | Cetaphil   |
