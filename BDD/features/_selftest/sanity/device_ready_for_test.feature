Feature: check if device is ready
  Background: a strange environment for device and host
    Given Target device is T1 "VZHGLMA742804186"

  @setup
  Scenario: check if device is ready, contribute the step "Test setup is ready "
    Given adb binary is available
    Given appium is running

    Given Fastboot init
    Given FASTBOOT Erase userdata
      And ADB Wait for device, timeout 600 seconds

      # about 600 for T1
      # about 900 for M812
      And ADB check boot completed, timeout 1200 seconds

    Then Wait for handy initialization
    # TODO: resume
    # And inject wifi configuration WIFI_CONFIG_TINKLABS_WTTQA
      And ADB Initialize android
