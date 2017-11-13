# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


caps = {}
caps["deviceName"] = "android"
caps["appPackage"] = "com.tinklabs.launcher"
caps["appActivity"] = ".features.main.activity.LauncherActivity"
caps["platformName"] = "android"

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

TouchAction(driver).press({x: 359, y: 1100}).moveTo({x: 263, y: -7}).release()


driver.quit()
