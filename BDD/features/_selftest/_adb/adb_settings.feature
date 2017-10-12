
@adb_command
Feature: self test for adb-handy-appium
  Background: scratch background
    Given Target device is T1 "VZHGLMA742804186"
    Given ADB push tinklabs1001
    And ADB push change_settings
    And ADB change permission tinklabs1001

  @test_adb_settings @package_verifier_enable
  Scenario: change settings value
    # Given ADB Init session
    And ADB settings put global package_verifier_enable 0
    Then ADB settings global package_verifier_enable should be 0
  # Given ADB adb shell test

  @test_adb_settings @package_verifier_enable
  Scenario: android settings
    Given ADB settings put global package_verifier_enable 0
    Then ADB settings global package_verifier_enable should be 0
    Given ADB settings put global package_verifier_enable 1
    Then ADB settings global package_verifier_enable should be 1
    Given ADB settings put global package_verifier_enable 0
    Then ADB settings global package_verifier_enable should be 0

