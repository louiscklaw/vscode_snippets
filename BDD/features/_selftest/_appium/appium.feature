
@appium_command
Feature: appium

  @test_appium
  Scenario: process wanted exist
    # Given ADB Init session
    Given appium is running

  Scenario: process wanted is not exist
    # Given ADB Init session
    Given NotAProcess is running

  @sanity @appium
  Scenario: Sanity check for the appium setup on behave side
    Given Target device is T1 "VZHGLMA742804186"
      And ADB initialize android
    Given setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds
