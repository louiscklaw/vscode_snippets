Feature: adb root shell
  Scenario: test adb root shell
    Given Target device is T1 "VZHGLMA742804186"
    Given adb root shell "settings put global package_verifier_enable 0"
