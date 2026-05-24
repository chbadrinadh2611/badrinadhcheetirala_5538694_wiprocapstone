@e2e
Feature: Guest Checkout Flow on Nykaa

  Background:
    Given I open the Nykaa Baby Care page

  @checkout @smoke
  Scenario: Complete guest checkout flow
    When I click on the first product
    And I check product is not out of stock
    And I add the product to the bag
    And I proceed to checkout
    And I continue as guest
    And I fill the shipping address
    Then the checkout page should be displayed