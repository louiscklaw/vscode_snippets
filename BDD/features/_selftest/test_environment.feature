Feature: test the strange environment
  Background: setup test environment on strange machine
    Given Target device is T1 "VZHGLMA742800785"

  @test_testenvironment
  Scenario: appium on strange environment
      Given ADB initialize android
      Given setup an android as below, using appium port 4723
        | Package                  | Activity                        | platform | type  | version |
        | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "300" seconds
