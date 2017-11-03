Feature: appium screen capture

  # behave -vk --no-capture --tags=test_appium_screen_capture .
  @test_appium_screen_capture
  Scenario: test appium screen capture
    Given Target device is T1 "VZHGLMA742800785"
    And ADB initialize android
    Given setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

    Given test appium screen capture


  @appium_capture_failed_screen
    Scenario: test capture failure screen
      Given Target device is T1 "VZHGLMA742800785"
      And ADB initialize android
      Given setup an android as below, using appium port 4723
        | Package                  | Activity                        | platform | type  | version |
        | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "300" seconds

      Given appium capture failed screen
