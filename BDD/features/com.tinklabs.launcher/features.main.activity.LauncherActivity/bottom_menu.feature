# -- FILE:    feature/features.main.activity.LauncherActivity
# apk:        /system/priv-app/com.tinklabs.launcher/base.apk
# package:    ccom.tinklabs.launcher
# activity:   features.main.activity.LauncherActivity

#{
#  "platformName": "Android",
#  "deviceName": "Android",
#  "appPackage": "com.tinklabs.launcher",
#  "appActivity": "features.main.activity.LauncherActivity"
#}

@com.tinklabs.launcher
@features.main.activity.LauncherActivity
Feature: sanity check for bottom menu
  Tap each items on the menu
  Validate correct page shown
  Scroll up / down on each listing / detail screen
  Background: scratch background
    Given setup an android as below
    | Package               | Activity                                 | platform | type  | version |
    | com.tinklabs.launcher | .features.main.activity.LauncherActivity | Android  | phone | 7.0     |
      And press HOME button
        And sleep 3 seconds
      And Wait until "Home" appears on screen, timeout "180" seconds

  Scenario:  button tour
    # And finish LauncherActivity tutorial
    # And sleep 1 seconds

    # Position from left to right
    Then Fail if buttons on the list below not appear at the position with id "com.tinklabs.launcher:id/button_ll"
      | button     | position |
      | Home       | 1        |
      | Apps       | 2        |
      | City Guide | 3        |
      | Shop       | 4        |
      | Tickets    | 5        |
      | Call       | 6        |
      # And Fail if "Apps" buttons not appears at the position "2"

  Scenario: Activate phone from launcher
    Given User tap on "Call" button
    Then Fail if the Text "handy phone" not appears on screen

  Scenario: Activate Home button
    # NOTE to check if the browser shown up
    Then Fail if the Text "Home" not appears on screen
    Then Swipe "com.tinklabs.launcher:id/mdContent" UP Distance "400" until "Yesterday" appears on screen (max swipe "100")

    # Check after work
    Then Fail if the Text "Home" not appears on screen

  Scenario: Activate App Drawer
    Given User tap on "Apps" button
      And sleep 1 seconds

    # Check at least the "RECENTLY USED" appears on screen
    # Then Fail if the Text "RECENTLY USED" not appears on screen
    Then Fail if the Text "handy phone" not appears on screen
    Then Fail if the Text "Play Store" not appears on screen

  Scenario: Swipe in App Drawer
    Given User tap on "Apps" button
      And sleep 1 seconds

      Then Swipe "com.tinklabs.launcher:id/main_app_list" UP Distance "400" until "Erase Data" appears on screen (max swipe "100")

  Scenario: Search in App Drawer
    Given User tap on "Apps" button

    # Just try a simple search
    Then tap on text "Search"
      # Uncertancy, need to tap Search again
      And tap on text "Search"
      And type "handy phone" in "com.tinklabs.launcher:id/search_et"

    Then Fail if the Text "handy phone" not appears on screen



