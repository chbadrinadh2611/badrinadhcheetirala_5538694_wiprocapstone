@positive
Feature: Rating Filter on Nykaa Baby Care

  Background:
    Given I open the Nykaa Baby Care page

  @rating @smoke
  Scenario Outline: Apply rating filter and validate products
    When I expand the Avg Customer Rating filter
    And I select the rating "<rating>"
    Then products should be displayed on the page

    Examples:
      | rating           |
      | 4 Stars & Above  |
      | 3 Stars & Above  |
