# com.tinklabs.activateapp/com.tinklabs.activateapp.features.client.return_device.ClientReturnActivity

# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


caps = {}
caps["deviceName"] = "android"
caps["appPackage"] = "com.tinklabs.activateapp"
caps["appActivity"] = ".features.client.return_device.ClientReturnActivity"
caps["platformName"] = "android"

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)


driver.quit()
