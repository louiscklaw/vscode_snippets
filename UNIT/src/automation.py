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
import UNIT.res.general as handyConfig
from UTIL.basePO import PageObject
import homePO

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
        desired_caps['appPackage'] = handyConfig.pkg_launcher
        desired_caps['appActivity'] = handyConfig.act_launcher
        desired_caps['noReset'] = True
        # connect to appium server
        self.driver = webdriver.Remote(appiumServer, desired_caps)
        self.basePO = PageObject(self.driver)


    def tearDown(self):
        self.driver.quit()

    def test_case1(self):

        time.sleep(1)
        home = homePO.homePO(self.basePO)
        home.goToCallTab()



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
