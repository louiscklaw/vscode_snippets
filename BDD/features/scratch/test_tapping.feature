# -- FILE: features/com.tinklabs.activateapp
# apk:      com.tinklabs.activateapp_base.apk
# package:  com.tinklabs.activateapp
# activity: .features.wizard.WizardActivity

#{
#  "platformName": "Android",
#  "deviceName": "Android",
#  "appPackage": "com.tinklabs.launcher",
#  "appActivity": "com.tinklabs.launcher.features.main.activity.LauncherActivity"
#}

Feature: test for basic tapping feature
  Background: scratch background
    Given setup an android as below
    | Package                  | Activity                        |  platform | type  |version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity |  Android  | phone |7.0     |
      And Wait for "Waiting for network connection..." ("10" countdown)
      And Wait for "Initializing..." ("20" countdown)
      And Wait for "checking for update..." ("10" countdown)
      And sleep 20 seconds

  @wip
  Scenario: Sanity test for Wizard activation
    Given Reach "The end" page in WizardActivity by skip
      And sleep 999

