
Feature: random click for a hour, pilot run
  @initialize_rom
  Scenario: initialize
    Given Target device is M812 "V2HGLMB721301100"
    And Test setup is ready

    Given setup an android as below, using appium port 4725
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "600" seconds
    Given Reach "Happy flow The end" page in WizardActivity by skip, route "THIS_TEXT_IS_RESERVED_FOR_LATTER_USE"
    And Skip the 1st time tutorial by launcher

    Then Random tour for 0.5 hour

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB check boot completed, timeout 600 seconds
    Then Wait for handy initialization
    And ADB Initialize android
    And setup an android as below, using appium port 4725
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "600" seconds
