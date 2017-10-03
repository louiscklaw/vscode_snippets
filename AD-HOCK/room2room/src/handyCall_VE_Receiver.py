# coding:utf-8
import os
import time
import unittest
from appium import webdriver
import collections

import sys
sys.path.append(os.path.dirname(os.path.normpath(sys.path[0])) + "/lib")
sys.path.append(os.path.dirname(os.path.normpath(sys.path[0])) + "/res")

import util as ul
import handy_element as el
import handyconfig

pyVesion = str(sys.version_info)
if 'major=2' in pyVesion:
    import HTMLTestRunner_2 as HTMLTestRunner
else:
    import HTMLTestRunner

# Returns abs path relative to this file and not cwd
# PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

parentFolder = os.path.dirname(os.path.normpath(sys.path[0]))


def PATH(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def checkFolder():
    today = time.strftime("%Y%m%d")
    if not os.path.exists(parentFolder + "/result" + today):
        os.makedirs(parentFolder + "/result" + today)
    return parentFolder + "/result" + today + "/"


# get device info by udid
Result = ul.getDeviceStatus(handyconfig.receiverDevice)

class Phone_Call(unittest.TestCase):

    def setUp(self):
        print("start to execute setup")
        ul.osCommand('cat "" > receiver_result')
        ul.osCommand('adb -s ' + handyconfig.receiverDevice + ' shell settings put global package_verifier_enable 0')
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = Result["Androidversion"]
        desired_caps['deviceName'] = Result["SerialNo"].replace('\r','')
        desired_caps['udid'] = Result['SerialNo'].replace('\r','')
        desired_caps['appPackage'] = el.Package['appPackage']
        desired_caps['appActivity'] = el.Package['appActivity']
        desired_caps['noReset'] = True
        # if 'M808' in Result['Model']:
        #     desired_caps['appPackage'] = el.Package['appPackage']
        #     desired_caps['appActivity'] = el.Package['appActivity_M808']
        self.driver = webdriver.Remote('http://localhost:4725/wd/hub', desired_caps)
        self.util = ul.Util(self.driver, parentFolder + "/screenshots/" + str(time.strftime("%Y%m%d")))
        print("Device Battery Level")
        ul.osCommand('adb -s ' + handyconfig.receiverDevice + ' shell dumpsys battery | grep level | head -1')
        print("Device Info")
        ul.osCommand('adb -s ' + handyconfig.receiverDevice + ' shell getprop | grep -i operator')

    def tearDown(self):
        ul.osCommand("adb -s " + handyconfig.receiverDevice + " shell input keyevent KEYCODE_ENDCALL")
        self.driver.quit()

    def test_roomToRoom_Receiver(self):
        try:
            receiverGetPhysicalVENumber = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['name'], 'get physical VE number', 240)
            receiverGetVECallStat = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['state'], 'get call receiver state')
            receiverGetVECallType = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['phoneNumber'], 'get call receiver state')

            verifyStrFromDut = (receiverGetPhysicalVENumber.text).replace(" ", "") + (receiverGetVECallType.text).upper() + (receiverGetVECallStat.text).upper()
            expectStr = handyconfig.VEPhysicalNumber + "SHEFFIELD" + "INCOMING CALL"

            result = self.util.isMatch(verifyStrFromDut, expectStr)
            ul.osCommand('echo ' + str(result) + ' > receiver_result')

            self.assertEqual(verifyStrFromDut, expectStr)

        except Exception as e:
            print(e)
            self.util.screenshot('VE_Receiver')
            self.assertTrue(False)


if __name__ == '__main__':
    checkFolder()
    today = time.strftime("%Y%m%d")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite((
        loader.loadTestsFromTestCase(Phone_Call)
    ))

    # unittest.TextTestRunner(verbosity=2).run(suite)

    # for HTMLTestRunner
    file = open(str(PATH(checkFolder() + (time.strftime("%Y%m%d-%H%M%S") + '_VE_Receiver.html'))), "wb")

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=file,
        title="[PG Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']',
        description="[Platform Version: " + Result["Androidversion"] + ']' + "[SDK version: " + Result["SDKversion"] + ']' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    # runner.run(suite_Normal)

    file.close()
