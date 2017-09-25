# -- FILE:    feature/.ApiDemos
# package:    ccom.tinklabs.launcher
# activity:   .ApiDemos

#{
#  "platformName": "Android",
#  "deviceName": "Android",
#  "appPackage": "com.example.android.apis",
#  "appActivity": ".ApiDemos"
#}

@scratch
Feature: APIdemo superb basic test route 1
  Background: testing on T1
    Given setup an android as below
      | Package                  | Activity  | type  | platform | version |
      | com.example.android.apis | .ApiDemos | phone | Android  | 7.0     |
    And sleep 3 seconds

  Scenario: Sanity test for launcher tutorial activation
    # Given started package "<Package>" activity "<Activity>" on "<platform>" type "<type>" ver "<version>"
    #   and sleep 1 seconds

    And press HOME button

    # Examples: Android kind
    #   | Package                  | Activity  | type  | platform | version |
    #   | com.example.android.apis | .ApiDemos | phone | Android  | 7.0     |

