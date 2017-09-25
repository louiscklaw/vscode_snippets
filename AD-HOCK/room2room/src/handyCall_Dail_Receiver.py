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
        if not os.path.exists(parentFolder + "/result"):
            os.makedirs(parentFolder + "/result")


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

    def tearDown(self):
        ul.osCommand("adb -s " + handyconfig.receiverDevice + " shell input keyevent KEYCODE_ENDCALL")
        self.driver.quit()

    def test_Dail_A_PhoneCall_Receiver(self):
        try:
            receiverGetPhoneCallNumber = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['phoneNumber'], 'get sender number in receiver', 240)
            receiverGetPhoneCallStat = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['state'], 'get call receiver state')
            result = self.util.isMatch((receiverGetPhoneCallNumber.text).replace(" ","") + (receiverGetPhoneCallStat.text).upper(), handyconfig.SenderNumber_sim + 'INCOMING CALL')
            ul.osCommand('echo ' + str(result) + ' > receiver_result')
            self.assertEqual((receiverGetPhoneCallNumber.text).replace(" ","") + (receiverGetPhoneCallStat.text).upper(), handyconfig.SenderNumber_sim + 'INCOMING CALL')

        except Exception as e:
            print(e)
            self.util.screenshot('dailAPhoneCall_Receiver')
            self.assertTrue(False)


if __name__ == '__main__':
    checkFolder()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite((
        loader.loadTestsFromTestCase(Phone_Call)
    ))

    # unittest.TextTestRunner(verbosity=2).run(suite)

    # for HTMLTestRunner
    file = open(str(PATH(parentFolder + '/result/' + str(time.strftime("%Y%m%d-%H:%M:%S") + '_Dail_Receiver.html'))), "wb")

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=file,
        title="[PG Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']',
        description="[Platform Version: " + Result["Androidversion"] + ']' + "[SDK version: " + Result["SDKversion"] + ']' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    # runner.run(suite_Normal)

    file.close()
