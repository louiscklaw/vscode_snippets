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
    Given Target device is T1 "VZHGLMA742804186"
    # Given appium is running
    # Given FASTBOOT Erase userdata
    # And ADB Wait for device, timeout 60 seconds
    # And ADB check boot completed, timeout 600 seconds
    # Then Wait for handy initialization
    # And ADB Initialize android
    # And ADB PATH_ANDROID_TEMP directory is ready, timeout 60 seconds
    Given ADB Initialize android
    Given setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    # 180 seconds, assume no update/OTA pending
    And Wait until "English" appears on screen, timeout "300" seconds
    Given Reach "Happy flow The end" page in WizardActivity by skip, route "THIS_TEXT_IS_RESERVED_FOR_LATTER_USE"
    And Skip the 1st time tutorial by launcher

  @test_quick_selftest
  @sanity
  Scenario: test both end
    POC of the random-click-1-hour test
    # the main random loop occurs here, ignore for the "must pass" case

    Then Random tour for 0.5 hour

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

  @test_route
  @sanity
  Scenario: test both end
    testing of the route used by the random-click-1-hour
    # the main random loop occurs here, ignore for the "must pass" case

    Then Random tour selftest, route 0
    Then Random tour selftest, route 1
    Then Random tour selftest, route 2
    Then Random tour selftest, route 3
    Then Random tour selftest, route 4

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

  @test_endtoend
  @sanity
  Scenario: test both end
    test the setup/destroy of the random-click-1-hour test
    # the main random loop occurs here, ignore for the "must pass" case

    Then sleep 5 seconds
    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

  @test_swipe_feed
  @test_swipe_feed_survey
  Scenario: Swipe the feed until Survey appears
    test the route Survey
    Then Swipe the feed until Survey appears

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds


  @test_swipe_feed
  @test_swipe_feed_discount_tickets
  Scenario: Swipe the feed until DISCOUNT TICKETS appears
    test the route DISCOUNT TICKETS

    Then Swipe the feed until DISCOUNT TICKETS appears

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds


  @test_swipe_feed
  @test_swipe_feed_trending
  Scenario: Swipe the feed until TRENDING appears
    test the route TRENDING
    Then Swipe the feed until TRENDING appears

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

  @test_swipe_feed
  @test_swipe_feed_fun_facts
  Scenario: Swipe the feed until fun facts appears
    Then Swipe the feed until FUN FACTS appears

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds



  @test_swipe_feed
  @test_swipe_feed_long
  Scenario: Swipe the feed until days ago appears
    obsoleted route "days ago"
    Then Swipe the feed until days ago appears

    Then In launcher side menu, Erase data
    # unconditional wait due to loss connection to the phone
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

  @test_app_drawer
  Scenario: Activate App Drawer from launcher
    test the route App Drawer
    Then Activate App Drawer from launcher

    Then In launcher side menu, Erase data
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds


  @test_app_drawer
  Scenario: Swipe up in App Drawer until Erase Data appears
    test the route App Drawer
    Then Swipe up in App Drawer until "Erase Data" appears

    Then In launcher side menu, Erase data
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds


  @test_erase_data
  Scenario: Just want to see for the step to handle the phone restart
    Then In launcher side menu, Erase data
    And sleep 180 seconds

    Then ADB Wait for device
    And ADB Initialize android
    And setup an android as below, using appium port 4723
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    And Wait until "English" appears on screen, timeout "300" seconds

# I am expecting the screen is the 1st page of WizardActivity
