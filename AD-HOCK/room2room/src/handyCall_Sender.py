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


# Result = dict (Manufacturer,Model,Brand,Androidversion,SDKversion,SerialNo)
Result = ul.getDeviceStatus(handyconfig.senderDevice)


class Phone_Call(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = Result["Androidversion"]
        desired_caps['deviceName'] = Result["SerialNo"]
        if Result['Model'] == 'VZH':
            desired_caps['appPackage'] = el.Package['appPackage']
            desired_caps['appActivity'] = el.Package['appActivity']
        if 'M808' in Result['Model']:
            desired_caps['appPackage'] = el.Package['appPackage']
            desired_caps['appActivity'] = el.Package['appActivity_M808']

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.util = ul.Util(self.driver, parentFolder + "/screenshots/" + str(time.strftime("%Y%m%d")))

    def tearDown(self):
        ul.osCommand("adb -s " + handyconfig.senderDevice + " shell input keyevent KEYCODE_ENDCALL")
        self.driver.quit()

    def test_roomToRoom(self):
        try:
            window_size = self.driver.get_window_size()
            max_width = window_size["width"]
            max_height = window_size['height']
            self.driver.swipe(max_width/2, max_height-10, max_width-10, max_height-10, 300)
            # cmd = 'adb shell input swipe ' + str(max_width/2) + " 10 " + str(max_width-10) + " 10"
            # ul.osCommand(cmd)
            # ul.osCommand("adb -s " + handyconfig.senderDevice + " shell input keyevent KEYCODE_BACK")
            time.sleep(1)
            self.util.waitUntilAndGetElement('text', el.handyPhone_tab_byString['phonebook'], 'click phone book').click()
            time.sleep(1)
            self.util.waitUntilAndGetElement('text', el.handyPhoneBook_function_byString['r2r'], 'click room to room').click()
            for number in str(handyconfig.r2rReceiverNumber):
                self.util.waitUntilAndGetElement('text', number, 'click '+ number).click()
                # time.sleep()
            # ul.osCommand("adb shell input keyevent KEYCODE_BACK")
            self.util.waitUntilAndGetElement('id', el.handyPhoneDialler_pannel_byRID['call'], 'click send button').click()
            callOutNumber = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['RoomNumber'], 'get call out number', 5)
            callOutState = self.util.waitUntilAndGetElement('id', el.androidDialler_pannel_byRid['state'], 'get call out state')

            times = 0
            with open('receiver_result', 'r') as content_file:
                self.receiver_result = content_file.read()
                content_file.close
            while self.receiver_result is "" or times < 3:
                time.sleep(5)
                times += 1
                with open('receiver_result', 'r') as content_file:
                    self.receiver_result = content_file.read()
                    content_file.close
            self.assertEqual(callOutNumber.text + callOutState.text + self.receiver_result, "Room " + handyconfig.r2rReceiverNumber + 'DIALING' + 'True\n')

        except Exception as e:
            print(e)
            self.util.screenshot('roomToRoom_Sender')
            self.assertTrue(False)


if __name__ == '__main__':
    checkFolder()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite((
        loader.loadTestsFromTestCase(Phone_Call)
    ))

    # unittest.TextTestRunner(verbosity=2).run(suite)

    # for HTMLTestRunner
    file = open(str(PATH(parentFolder + '/result/' + "Sender_" + str(time.strftime("%Y%m%d%H%M%S") + '.html'))), "wb")

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=file,
        title="[PG Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']',
        description="[Platform Version: " + Result["Androidversion"] + ']' + "[SDK version: " + Result["SDKversion"] + ']' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    # runner.run(suite_Normal)

    file.close()
