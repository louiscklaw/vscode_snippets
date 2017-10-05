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

@random-click-1-hour
Feature: test single step from random-click-1-hour
  Background: scratch background
    Given appium is running
    Given FASTBOOT Erase userdata
      And ADB Wait for device, timeout 60 seconds
      And ADB check boot completed, timeout 600 seconds
    Then Wait for handy initialization
      And ADB Initialize android
      # And ADB PATH_ANDROID_TEMP directory is ready, timeout 60 seconds

    Given setup an android as below
    | Package                  | Activity                        | platform | type  | version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      # 180 seconds, assume no update/OTA pending
      And Wait until "English" appears on screen, timeout "180" seconds
    Given Reach "Happy flow The end" page in WizardActivity by skip
      And Skip the 1st time tutorial by launcher

  @test_endtoend
  @sanity
  Scenario: test both end
    Description try to validate the skeleton for the test
      # the main random loop occurs here, ignore for the "must pass" case

    Then sleep 5 seconds
    Then In launcher side menu, Erase data
      # unconditional wait due to loss connection to the phone
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

  @test_swipe_feed
  @test_swipe_feed_short
  Scenario: Swipe the feed until hours ago appears
    Then Swipe the feed until hours ago appears

    Then In launcher side menu, Erase data
      # unconditional wait due to loss connection to the phone
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

  @test_swipe_feed
  @test_swipe_feed_long
  Scenario: Swipe the feed until Yesterday appears
    Then Swipe the feed until Yesterday appears

    Then In launcher side menu, Erase data
      # unconditional wait due to loss connection to the phone
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

  @test_app_drawer
  Scenario: Activate App Drawer from launcher
    Then Activate App Drawer from launcher

    Then In launcher side menu, Erase data
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds


  @test_app_drawer
  Scenario: Swipe up in App Drawer until Erase Data appears
    Then Swipe up in App Drawer until "Erase Data" appears

    Then In launcher side menu, Erase data
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds


  @test_erase_data
  Scenario: Just want to see for the step to handle the phone restart
    Then In launcher side menu, Erase data
      And sleep 180 seconds

    Then ADB Wait for device
      And ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

    # I am expecting the screen is the 1st page of WizardActivity
