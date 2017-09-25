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
    Given setup an android as below
    | Package               | Activity                                 | platform | type  | version |
    | com.tinklabs.launcher | .features.main.activity.LauncherActivity |  Android  | phone |7.0     |
      # TODO: Temporary using Home button as the indicator. until have a better idea
      And Wait until "Home" appears on screen, timeout "180" seconds

  Scenario: erase data from launcher
    # Given In launcher side menu, Erase data
    Then press HOME button
      And tap hamburger button on launcher
      And Swipe the menu UP until "Erase Data" appears on screen (max swipe "15")

      # select Erase Data in menu
      And tap on text "Erase Data"

    Then Wait until "Erase Data" appears on screen, timeout "30" seconds
      # NOTE check the cancel flow
      # And tap on text "CANCEL"

      # NOTE given that i want to erase data
      And tap on text "ERASE DATA"
      And Wait until "Confirmation" appears on screen, timeout "30" seconds
      And tap on text "YES"
