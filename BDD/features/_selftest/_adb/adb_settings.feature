
@adb_command @integration
Feature: self test for adb-handy-appium
  Background: scratch background
    Given Target device is T1 "VZHGLMA742804186"
    Given ADB push tinklabs1001
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
