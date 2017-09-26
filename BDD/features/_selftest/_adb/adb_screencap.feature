@adb_command
Feature: self test for adb-handy-appium
  Background: scratch background
    Given FASTBOOT Erase userdata
      And ADB Wait for device, timeout 60 seconds
    Then ADB check boot completed, timeout 600 seconds

  @adb_shell
  @test_adb_screen_capture
  Scenario: android screen capture, save to filename
    Given ADB screen capture, save to "./_temp/Pass_picture"
