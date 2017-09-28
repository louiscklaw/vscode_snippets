@test_rom_sanity
Feature: Rom can wake the phone
  Background: scratch background
    Given Clear all handy settings
      And ADB Wait for device, timeout 60 seconds
    Then ADB check boot completed, timeout 600 seconds
      And ADB Initialize android

  Scenario: try to reach welcome page using ROM
    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      # 180 seconds, assume no update/OTA pending
      And Wait until "English" appears on screen, timeout "300" seconds

