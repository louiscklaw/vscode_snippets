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

@fastboot
Feature: FASTBOOT wrapper
  Background: scratch background
    Given ADB Wait for device, timeout 60 seconds

    @fastboot_clear_userdata_only
    Scenario: test procedure to clear userdata only
      Given ADB Reboot bootloader
        And FASTBOOT unlock
        Then FASTBOOT "-i 0x489 erase userdata"
        Then FASTBOOT "reboot"

    @fastboot_clear_user_data
    Scenario: test procedure to erase userdata
      Given ADB Reboot bootloader

      Then FASTBOOT "-i 0x489 oem fih on"
      Then FASTBOOT "-i 0x489 oem devlock key"
      Then FASTBOOT "-i 0x489 erase userdata"
      Then FASTBOOT "-i 0x489 erase oem"
      Then FASTBOOT "reboot"

    @fastboot_clear_user_data_oneline
    Scenario: test packed procedure
      Given FASTBOOT Erase userdata


    @fastboot_download_image
    Scenario: test download image
      Given ADB Reboot bootloader

      Then FASTBOOT "-i 0x489 oem fih on"
      Then FASTBOOT "-i 0x489 oem devlock key"

      Then FASTBOOT "-i 0x489 erase userdata"
      Then FASTBOOT "-i 0x489 erase oem"

      Then FASTBOOT "-i 0x489 flash system /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/handy-VZH-0-026A-00WW-system-1504271348.img", timeout 180 seconds
      Then FASTBOOT "-i 0x489 flash boot /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/boot-handy-adb-root-signed.img", timeout 60 seconds
      Then FASTBOOT "-i 0x489 flash recovery /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/handy-VZH-0-026A-00WW-recovery-0724.img", timeout 60 seconds
      Then FASTBOOT "-i 0x489 flash cda /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/VZH-00WW-004-cda.img", timeout 60 seconds

      Then FASTBOOT "reboot"
#VZH-00WW-004-cda.img

    @fastboot_download_image_oneline
    Scenario: test packed procedure for download image
      Given FASTBOOT download image
