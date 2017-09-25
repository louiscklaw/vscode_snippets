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
    Given ADB change package_verifier_enable = 0
    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.launcher | .features.main.activity.LauncherActivity |  Android  | phone |7.0     |
      And Wait until "Home" appears on screen, timeout "180" seconds

  Scenario: try1
    Then Try to activate handy phone from launcher

  Scenario: try2
    Then Activate App Drawer from launcher

  Scenario: try3
    Then Swipe up in App Drawer until "Google" appears

  @wip
  Scenario: try4
    Then Click on a random clickable and sleep 10 seconds
