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
Feature: Wizard activation UI route 1
  Background: scratch background
    Given setup an android as below
    | Package               | Activity                                 | platform | type  | version |
    | com.tinklabs.launcher | .features.main.activity.LauncherActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

  Scenario: Sanity test for launcher tutorial activation
    # Tap_this_show_the_hostel_details
    Then Fail if the "Tap this show the hotel details." not appears on screen
      and Tap screen 1 times at CENTER

    # Tap_on_this_icon_to_open_the_side_bar
    # com.tinklabs.launcher:id/click_through means back button on the top-left
    Then Fail if the "Tap on this icon to open the side bar." not appears on screen
      and tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"

    # Scroll_down_to_explore_all_the_main_features_of_handy
    Then Fail if the "Scroll down to explore all the main features of handy." not appears on screen
      and tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"

    # Shop_for_discounted_souvenirs
    Then Fail if the "Shop for discounted souvenirs and the hottest new products, and enjoy free delivery." not appears on screen
      and tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"

    # Tours_and_tickets_to_major_attractions
    Then Fail if the "Tours and tickets to major attractions - all available here at a discount.Tours and tickets to major attractions - all available here at a discount." not appears on screen
      and tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
