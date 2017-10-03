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
Result = ul.getDeviceStatus(handyconfig.senderDevice)


class Phone_Call(unittest.TestCase):

    def setUp(self):
        ul.osCommand('adb -s ' + handyconfig.senderDevice + ' shell settings put global package_verifier_enable 0')
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

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.util = ul.Util(self.driver, parentFolder + "/screenshots/" + str(time.strftime("%Y%m%d")))

        print("Device Battery Level")
        ul.osCommand('adb -s ' + handyconfig.senderDevice + ' shell dumpsys battery | grep level | head -1')
        print("Device Info")
        ul.osCommand('adb -s ' + handyconfig.senderDevice + ' shell getprop | grep -i operator')

    def tearDown(self):
        ul.osCommand("adb -s " + handyconfig.senderDevice + " shell input keyevent KEYCODE_ENDCALL")
        self.driver.quit()

    def test_Dail_A_PhoneCall_Sender(self):
        try:
            # step 1 unlock screen
            window_size = self.driver.get_window_size()
            max_width = window_size["width"]
            max_height = window_size['height']
            self.driver.swipe(max_width/2, max_height-10, max_width-10, max_height-10, 300)
            time.sleep(1)

            # step 2 click phone book then click Local Call
            self.util.waitUntilAndGetElement('text', el.handyPhone_tab_byString['phonebook'], 'click phone book').click()
            time.sleep(2)
            self.util.waitUntilAndGetElement('text', el.handyPhoneBook_function_byString['local'], 'click Local Call').click()

            # step 3 click receiver room number
            for number in str(handyconfig.ReceiverNumber_sim):
                self.util.waitUntilAndGetElement('text', number, 'click '+ number).click()

            # step 4 click send
            self.util.waitUntilAndGetElement('id', el.handyPhoneDialler_pannel_byRID['call'], 'click send button').click()

            # step 5 get receiver info
            callOutNumber = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['name'], 'get call out number', 5)
            callOutState = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['state'], 'get call out state')
            verifyStr = (callOutNumber.text).replace(" ", "") + callOutState.text

            # step 6 get receiver result and confirm the total test result
            times = 0
            with open('receiver_result', 'r') as content_file:
                self.receiver_result = content_file.read()
                content_file.close
            while self.receiver_result == "" or times < 5:
                time.sleep(3)
                times += 1
                with open('receiver_result', 'r') as content_file:
                    self.receiver_result = content_file.read()
                    content_file.close
            self.assertEqual(verifyStr + self.receiver_result, handyconfig.ReceiverNumber_sim + 'DIALING' + 'True\n')

        except Exception as e:
            print(e)
            self.util.screenshot('dailAPhoneCall_Sender')
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
    file = open(str(PATH(checkFolder() + (time.strftime("%Y%m%d-%H%M%S") + '_Dial_Sender.html'))), "wb")

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=file,
        title="[PG Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']',
        description="[Platform Version: " + Result["Androidversion"] + ']' + "[SDK version: " + Result["SDKversion"] + ']' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    # runner.run(suite_Normal)

    file.close()
