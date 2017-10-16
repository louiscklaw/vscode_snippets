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
    Given Target device is T1 "VZHGLMA742804186"
    Given setup an android as below, using appium port 4723
      | Package               | Activity                                 | platform | type  | version |
      | com.tinklabs.launcher | .features.main.activity.LauncherActivity | Android  | phone | 7.0     |
    # TODO: Temporary using Home button as the indicator. until have a better idea
    And Wait until "Home" appears on screen, timeout "180" seconds

  Scenario: erase data from launcher
    # Given In launcher side menu, Erase data
    Then In launcher side menu, Erase data
