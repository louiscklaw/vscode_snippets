
@appium_command
Feature: appium
  @test_appium
  Scenario: process wanted exist
    # Given ADB Init session
    Given appium is running
  Scenario: process wanted is not exist
    # Given ADB Init session
    Given NotAProcess is running
