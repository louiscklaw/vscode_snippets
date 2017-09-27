@test_rom_sanity
Feature: Erase data from launcher
  Background: scratch background
    Given FASTBOOT Erase userdata
      And ADB Wait for device, timeout 60 seconds
    Then ADB check boot completed, timeout 600 seconds
      And ADB Initialize android

  Scenario: ROM can wake up
    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      # 180 seconds, assume no update/OTA pending
      And Wait until "English" appears on screen, timeout "180" seconds

