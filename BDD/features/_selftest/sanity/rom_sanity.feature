@test_rom_sanity
Feature: Rom can wake the phone
  Background: scratch background
    Given Target device is T1 "VZHGLMA742804186"
    And Test setup is ready

  Scenario: try to reach welcome page using ROM
    Given setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    # 180 seconds, assume no update/OTA pending
    And Wait until "English" appears on screen, timeout "300" seconds

