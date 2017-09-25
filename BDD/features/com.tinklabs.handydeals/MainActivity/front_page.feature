# -- FILE:    com.tinklabs.handydeals/MainActivity
# apk:        /system/priv-app/com.tinklabs.handydeals/base.apk
# package:    com.tinklabs.handydeals
# activity:   MainActivity

#{
#  "platformName": "Android",
#  "deviceName": "Android",
#  "appPackage": "com.tinklabs.handydeals",
#  "appActivity": ".MainActivity"
#}

# Ref:
# https://docs.google.com/presentation/d/1sHDHTuVP2KsNQfRohYurV3lQVpBAC1e8hy4Hwollqxo/edit#slide=id.g1fab31fb3a_0_58

@com.tinklabs.handydeals
@MainActivity
Feature: sanity check Tickets
  Background: scratch background
    Given setup an android as below
    | Package                 | Activity      | platform | type  | version |
    | com.tinklabs.handydeals | .MainActivity | Android  | phone | 7.0     |
      And press HOME button
        And sleep 3 seconds
      And Wait until "Home" appears on screen, timeout "180" seconds

  Scenario:  button tour
    Given User tap on "Tickets" button
      And sleep 3 seconds

    # Position from left to right
    Then Fail if buttons on the list below not appear at the position with id "com.tinklabs.handydeals:id/bottomNatvigation"
      | button  | position |
      | Tickets | 1        |
      | Orders  | 2        |
      | Help    | 3        |
      # And Fail if "Apps" buttons not appears at the position "2"

  @wip
  Scenario: Activate Tickets button
    Given User tap on "Tickets" button
      And sleep 1 seconds

    Then Fail if the Text "Tickets" not appears on screen
    Then Fail if the Text "Search" not appears on screen


  Scenario: Try highlight deal
    Given User tap on "Tickets" button
      And sleep 1 seconds

    Then tap on highlight deal 1 in Tickets
      And tap on back arrow in highlight deals detail page

  # Scenario:

