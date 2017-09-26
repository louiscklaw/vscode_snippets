Feature: Erase data from launcher
  Background: scratch background
    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      # consider update ?
      And Wait until "English" appears on screen, timeout "180" seconds

  Scenario: android screen capture, save to "/tmp"
    Given ADB Init session
    Given ADB screen capture, save to "./_temp"
