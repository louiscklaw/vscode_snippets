# coding:utf-8
import os
import sys
import time
import unittest
from appium import webdriver


srcParentFolder = os.path.dirname(os.path.normpath(sys.path[0]))
unitParentFoler = os.path.dirname(os.path.normpath(srcParentFolder))
sys.path.append(unitParentFoler)
from UTIL.deviceInfo import DevicesInfo
import UTIL.utils as utils
from UTIL.basePO import PageObject

pyVesion = str(sys.version_info)
if 'major=2' in pyVesion:
    import UTIL.HTMLTestRunner_2 as HTMLTestRunner
else:
    import UTIL.HTMLTestRunner as HTMLTestRunner

deviceName = 'VZHGLMA742901452'
dut = DevicesInfo(deviceName)
manufacturer = dut.getManufacturer()
model = dut.getModel()
brand = dut.getBrand()
androidVersion = dut.getAndroidVersion()
sdkVersion = dut.getSDKVersion()
serialNo = dut.getSerialNo()

def PATH(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def checkReportFolder():
    today = time.strftime("%Y%m%d")
    reportPath = srcParentFolder + "/report/" + today
    if not os.path.exists(reportPath):
        os.makedirs(reportPath)
    return reportPath + "/"


class Demo(unittest.TestCase):
    def setUp(self):
        # avoid google block
        utils.osCommand('adb -s ' + deviceName + ' shell settings put global package_verifier_enable 0')
        # prepare to connect appium server
        appiumServer = 'http://localhost:4723/wd/hub'
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = androidVersion
        desired_caps['deviceName'] = serialNo
        desired_caps['udid'] = serialNo
        desired_caps['appPackage'] = 'com.tinklabs.handyphone'
        desired_caps['appActivity'] = 'com.tinklabs.handyphone.features.splash.SplashActivity'
        desired_caps['noReset'] = True
        # connect to appium server
        self.driver = webdriver.Remote(appiumServer, desired_caps)
        po = PageObject(self.driver)
        po.test()

    def tearDown(self):
        self.driver.quit()

    def test_case1(self):
        window_size = self.driver.get_window_size()
        max_width = window_size["width"]
        max_height = window_size['height']
        self.driver.swipe(max_width / 2, max_height - 10, max_width - 10, max_height - 10, 300)
        time.sleep(1)



if __name__ == '__main__':
    # create unit test loader and test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite((
        loader.loadTestsFromTestCase(Demo) # Use ',' to add the other loader.loadTestsFromTestCase(Demo),
    ))

    # for create Report file
    file = open(str(PATH(checkReportFolder() + (time.strftime("%Y%m%d-%H%M%S") + '.html'))), "wb")

    runner = HTMLTestRunner.HTMLTestRunner(
        stream = file,
        title = "[PG Automation] [Python+Appium] [Device: " + manufacturer + " " + model + ' ' + brand + "]",
        description = "[Platform Version: " + androidVersion + "]" + "[SDK version: " + sdkVersion + "]" + "[Device S/N: " + serialNo + "]"
    )
    runner.run(suite)
    file.close()
