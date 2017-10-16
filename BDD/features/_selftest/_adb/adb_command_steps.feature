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

@adb_command
Feature: self test for adb-handy-appium
  Background: scratch background
    Given Target device is T1 "VZHGLMA742804186"
    # Given FASTBOOT Erase userdata
    #   And ADB Wait for device, timeout 60 seconds
    # Then ADB check boot completed, timeout 600 seconds

  @test_adb_push_file
  Scenario: copy file from PC to android
    # Given ADB Init session
    Given ADB push tinklabs1001
      And ADB push change_settings

  @test_adb_change_permission
  Scenario: modify file permission
    # Given ADB Init session
    Given ADB push tinklabs1001
      And ADB change permission tinklabs1001

  @test_adb_settings_global
  Scenario: change settings value
    # Given ADB Init session
    Given ADB push tinklabs1001
      And ADB settings put global package_verifier_enable 0
    Then ADB settings global package_verifier_enable should be 0
    # Given ADB adb shell test

  @test_adb_settings_global
  Scenario: android settings
    Given ADB settings put global package_verifier_enable 0
    Then ADB settings global package_verifier_enable should be 0
    Given ADB settings put global package_verifier_enable 1
    Then ADB settings global package_verifier_enable should be 1
    Given ADB settings put global package_verifier_enable 0
    Then ADB settings global package_verifier_enable should be 0


  @test_adb_settings_system
  Scenario: change settings value
    # Given ADB Init session
    Given ADB push tinklabs1001
    And ADB settings put system screen_brightness 50
    Then ADB settings system screen_brightness should be 50
  # Given ADB adb shell test

  @test_adb_settings_system
  Scenario: android settings
    Given ADB settings put system screen_brightness 50
    Then ADB settings system screen_brightness should be 50
    Given ADB settings put system screen_brightness 10
    Then ADB settings system screen_brightness should be 10
    Given ADB settings put system screen_brightness 50
    Then ADB settings system screen_brightness should be 50


  @test_adb_settings_secure
  Scenario: change settings value
    # Given ADB Init session
    Given ADB push tinklabs1001
    And ADB settings put secure screensaver_enabled 0
    Then ADB settings secure screensaver_enabled should be 0
  # Given ADB adb shell test

  @test_adb_settings_secure
  Scenario: android settings
    Given ADB settings put secure screensaver_enabled 0
    Then ADB settings secure screensaver_enabled should be 0
    Given ADB settings put secure screensaver_enabled 1
    Then ADB settings secure screensaver_enabled should be 1
    Given ADB settings put secure screensaver_enabled 0
    Then ADB settings secure screensaver_enabled should be 0


  @in_the_middle
  @test_adb_props
  Scenario: android props
    Given ADB setprop "sys.usb.config" "mtp,adb"
      And sleep 1 seconds
      # sleep a while for the usb re-connect

    Given ADB setprop "persist.sys.usb.config" "adb,mtp"

    # Given ADB setprop "persist.sys.usb.config" "adb,mtp,mass_storage"
    # Then ADB prop "persist.sys.usb.config" should be "adb,mtp,mass_storage"
    # Given ADB setprop "persist.sys.usb.config" "adb,mtp"
    # Then ADB prop "persist.sys.usb.config" should be "adb,mtp"

  @test_adb_screen_capture
  Scenario: android screen capture, save to "/tmp"
    Given ADB screen capture, save to "./_temp"

  @test_adb_screen_record
  Scenario: android video capture, save to "/tmp"
    # Given ADB Init session
      And ADB video capture, save it to "/sdcard/testvideo.mp4"
      And sleep 5 seconds
      And ADB shell "input keyevent 3"
      And ADB shell "input tap 0 0"
      And sleep 5 seconds
      And ADB stop video capture process
      And ADB pull "/sdcard/testvideo.mp4" "/tmp"

  @test_initialize_device
  Scenario: test_initialize_device
    Given ADB Initialize android

  @test_adb_reboot_device
  Scenario: test_reboot_device
    # wait device for reboot
    Given ADB Reboot device
    Then ADB Wait for device, timeout 60 seconds
      And sleep 15 seconds
    Given ADB Initialize android
      And setup an android as below
      | Package                  | Activity                        | platform | type  | version |
      | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |

  @ADB_Initialize_android
  Scenario: check android initialize settings
    Given ADB settings put global package_verifier_enable 0
      And ADB settings put global stay_on_while_plugged_in 7
      And ADB settings put secure install_non_market_apps 1
      And ADB settings put secure screen_off_timeout 600000000
      And ADB settings put secure screensaver_activate_on_sleep 0
      And ADB settings put secure screensaver_components com.google.android.deskclock/com.android.deskclock.Screensaver
      And ADB settings put secure screensaver_default_component com.google.android.deskclock/com.android.deskclock.Screensaver
      And ADB settings put secure screensaver_enabled 0
      And ADB settings put system dim_screen 0
      And ADB settings put system screen_brightness 255
      And ADB settings put system screen_off_timeout 600000000
      And ADB settings put system transition_animation_scale 0
      And ADB settings put system window_animation_scale 0

      # disable USB file transfer
      # And ADB setprop "persist.sys.usb.config" "adb,mtp"
      # And ADB setprop test with shell True
    Then sleep 10 seconds



  @not_working
  @test_adb_setup_wifi
  Scenario: user want to setup wifi using ADB
    Given ADB setup wifi

# TODO: to turn on airplane mode
# settings put global airplane_mode_on 1
# am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true


# settings put global stay_on_while_plugged_in 7
