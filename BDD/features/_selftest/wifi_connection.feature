Feature: wifi connection

  @setup
  Scenario: test for insert the wifi configuration into android
    Given Target device is T1 "VZHGLMA742804186"
    Given ADB push tinklabs1001
    Given a file named "/tmp/tinklabs_wpa_supplicant.conf" with:
      """
      network={
      ssid="Tinklabs_WTTQA"
      psk="l@d1783o"
      key_mgmt=WPA-PSK
      priority=1
      }
      """
    Then ADB adb push "/tmp/tinklabs_wpa_supplicant.conf" "/data/local/tmp"
    And inject wifi configuration "/data/local/tmp/tinklabs_wpa_supplicant.conf" to android
    Then adb restart wifi
    And Fail if the android cannot ping to www.google.com
