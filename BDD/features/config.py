#!/usr/bin/env python
import os,sys

PATH_ADB_BINARY   = "/usr/local/bin/adb"
PATH_APPIUM_BINARY = r'/usr/local/bin/appium'


wifi_config={}

#steps to setup TINKLABS_WTTQA

wifi_config['WIFI_CONFIG_TINKLABS_WTTQA']=u'''
    Given ADB push tinklabs1001
    Given a file named "/Users/louis_law/.android_tinklabs/tinklabs_wpa_supplicant.conf" with:
        """
            network={
                ssid="Tinklabs_WTTQA"
                psk="l@d1783o"
                key_mgmt=WPA-PSK
                priority=1
            }
        """
    Then ADB adb push "/Users/louis_law/.android_tinklabs/tinklabs_wpa_supplicant.conf" "/data/local/tmp"
        And inject wifi configuration "/data/local/tmp/tinklabs_wpa_supplicant.conf" to android
    Then adb restart wifi
        And Fail if the android cannot ping to www.google.com
'''
