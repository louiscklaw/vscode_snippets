
Feature: random click for a hour
  @initialize_rom
  Scenario: initialize
    Given Target device is T1 "VZHGLMA742804186"
    And appium is running

    # TODO: resume
    Given Fastboot init
    And FASTBOOT Erase userdata

    Then ADB Wait for device, timeout 60 seconds
    And ADB check boot completed, timeout 600 seconds
    And Wait for handy initialization

    Then ADB Initialize android

    Given setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

    Given Reach "Happy flow The end" page in WizardActivity by skip, route "RESERVED_FOR_LATTER_USE"
    And Skip the 1st time tutorial by launcher

    Then Random tour for 0.001 hour

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB check boot completed, timeout 600 seconds
    Then Wait for handy initialization
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds
