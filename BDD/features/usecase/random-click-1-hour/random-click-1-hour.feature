# -- FILE: features/com.tinklabs.activateapp
# apk:      com.tinklabs.activateapp_base.apk
# package:    ccom.tinklabs.launcher
# activity:   features.main.activity.LauncherActivity

#{
#  "platformName": "Android",
#  "deviceName": "Android",
#  "appPackage": "com.tinklabs.launcher",
#  "appActivity": "com.tinklabs.launcher.features.main.activity.LauncherActivity"
#}


Feature: Erase data from launcher
  Background: scratch background
    Given ADB reboot device
      And ADB Wait for device, timeout 60 seconds
      And ADB Initialize android
    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      # consider update ?
      And Wait until "English" appears on screen, timeout "180" seconds

  @slow
  @usecase
  @long_duration
  Scenario: erase data from launcher
    Given Reach "Happy flow The end" page in WizardActivity by skip
      And Skip the 1st time tutorial by launcher

    Then Random tour for 0.02 hour

    Then In launcher side menu, Erase data
      # unconditional wait due to loss connection to the phone
      And sleep 180 seconds

    Then ADB Wait for device, timeout 60 seconds
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds
