@e2e
Feature: Add Product to Cart on Nykaa

  Background:
    Given I open the Nykaa Baby Care page

  @cart @smoke
  Scenario: Add first product to bag and validate cart
    When I click on the first product
    And I check product is not out of stock
    And I add the product to the bag
    Then the cart should reflect the added item