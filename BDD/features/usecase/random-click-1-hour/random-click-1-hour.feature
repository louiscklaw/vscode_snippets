@random_click_for_an_hour
Feature: Erase data from launcher
  Background: scratch background
    Given FASTBOOT Erase userdata
      And ADB Wait for device, timeout 60 seconds
    Then ADB check boot completed, timeout 600 seconds
      And ADB Initialize android

    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

    Given Reach "Happy flow The end" page in WizardActivity by skip
      And Skip the 1st time tutorial by launcher

  @slow
  @usecase
  @long_duration
  @random-click-1-hour
  Scenario: random tour for a long duration
    Then Random tour for 0.5 hour

    Then In launcher side menu, Erase data
      # unconditional wait due to loss connection to the phone
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds
