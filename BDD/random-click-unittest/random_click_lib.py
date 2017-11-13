#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint
import pexpect


import subprocess
import shlex
from threading import Timer


from time import sleep

from common_lib import *


from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction


from android_function import finger

from scheduler_lib import *

PROJ_HOME = os.path.dirname(__file__)
APK_HOME = os.path.sep.join([
    PROJ_HOME,
    '_apk'
])
PATH_PC_LIB = PROJ_HOME + '/../_lib/shell_script'
PATH_ANDROID_TEMP = r'/data/local/tmp'

FILE_TINKLABS1001 = r'tinklabs1001'
FILE_CHANGE_SETTINGS = r'change_settings.sh'
FILE_CHANGE_PROP = r'change_prop.sh'

FILE_CHANGE_WPA_SUPPLICANT = r'change_wifi.sh'
FILE_WPA_SUPPLICANT = r'wpa_supplicant.conf'

PATH_PC_TINKLABS1001 = '/'.join([PATH_PC_LIB, FILE_TINKLABS1001])
PATH_PC_CHANGE_SETTINGS = '/'.join([PATH_PC_LIB, FILE_CHANGE_SETTINGS])
PATH_PC_CHANGE_PROP = '/'.join([PATH_PC_LIB, FILE_CHANGE_PROP])

PATH_ANDROID_TINKLABS1001 = '/'.join([PATH_ANDROID_TEMP, FILE_TINKLABS1001])
PATH_ANDROID_CHANGE_SETTINGS = '/'.join(
    [PATH_ANDROID_TEMP, FILE_CHANGE_SETTINGS])
PATH_ANDROID_CHANGE_PROP = '/'.join([PATH_ANDROID_TEMP, FILE_CHANGE_PROP])

PATH_PC_WPA_SUPPLICANT_CONF = '/'.join([PATH_PC_LIB, FILE_WPA_SUPPLICANT])
PATH_PC_CHANGE_WPA_SUPPLICANT = '/'.join(
    [PATH_PC_LIB, FILE_CHANGE_WPA_SUPPLICANT])
PATH_ANDROID_CHANGE_WPA_SUPPLICANT = '/'.join(
    [PATH_ANDROID_TEMP, FILE_CHANGE_WPA_SUPPLICANT])

PATH_ANDROID_WIFI_WPA_SUPPLICANT = r'/data/misc/wifi/wpa_supplicant.conf'
PATH_ANDROID_WIFI_WPA_SUPPLICANT_BACKUP = r'/data/local/tmp/wpa_supplicant.bak'

dParameters = {}
dParameters['PATH_PC_LIB'] = PATH_PC_LIB
dParameters['PATH_PC_TINKLABS1001'] = PATH_PC_TINKLABS1001
dParameters['PATH_PC_CHANGE_SETTINGS'] = PATH_PC_CHANGE_SETTINGS
dParameters['PATH_PC_CHANGE_PROP'] = PATH_PC_CHANGE_PROP

dParameters['PATH_PC_WPA_SUPPLICANT_CONF'] = PATH_PC_WPA_SUPPLICANT_CONF
dParameters['PATH_PC_CHANGE_WPA_SUPPLICANT'] = PATH_PC_CHANGE_WPA_SUPPLICANT

dParameters['PATH_ANDROID_TEMP'] = PATH_ANDROID_TEMP
dParameters['PATH_ANDROID_TINKLABS1001'] = PATH_ANDROID_TINKLABS1001
dParameters['PATH_ANDROID_CHANGE_SETTINGS'] = PATH_ANDROID_CHANGE_SETTINGS
dParameters['PATH_ANDROID_CHANGE_PROP'] = PATH_ANDROID_CHANGE_PROP

dParameters['PATH_ANDROID_CHANGE_WPA_SUPPLICANT'] = PATH_ANDROID_CHANGE_WPA_SUPPLICANT


class handy_command:
    def __init__(self, device_model, android_serial, result_directory):
        self.android_serial = android_serial
        self.device_model = device_model
        self.result_directory = result_directory
        self.screencapture_directory = os.path.sep.join([
            self.result_directory, self.device_model, '_screencapture'
        ])
        pass

    def screencapture(self):
        """perform screen capture """
        try:
            # TODO: fine tune me
            logging.info('STEP: perform screencapture')
            screencapture_filename = getTodayString() + '-screencap.png'
            screencapture_on_computer = os.path.sep.join([
                self.screencapture_directory, screencapture_filename
            ])
            screencapture_on_android = os.path.sep.join([
                '/sdcard', screencapture_filename
            ])

            lsCommand = []
            lsCommand.append(self.construct_adb_command(
                'shell screencap -p %s' % screencapture_on_android))
            lsCommand.append(self.construct_adb_command(
                'pull %s %s' %
                (screencapture_on_android, screencapture_on_computer)))
            lsCommand.append(self.construct_adb_command(
                'shell rm %s' % screencapture_on_android))
            logging.debug('STEP: screencapture done')
            self.send_command(lsCommand)

        except Exception as e:
            logging.error('error during perform screencapture')
            raise e
        else:
            pass

    def unlockScreenHelper(self):
        try:
            # adb shell am start -n io.appium.unlock/.Unlock
            unlock_apk = os.path.join([
                APK_HOME,
                'unlock_apk-debug.apk'
            ])
            self.send_command(
                [   
                    self.construct_adb_command(
                        'shell install %s' % unlock_apk),
                    self.construct_adb_command(
                        'shell am start -n io.appium.unlock/.Unlock')
                ]
            )
            pass
        except Exception as e:
            logging.error('error during using unlockScreenHelper')
        else:
            pass

    def unLockScreen(self):
        try:
            window_size = self.appiumSession.get_window_size()
            max_width = window_size["width"]
            max_height = window_size['height']
            self.appiumSession.swipe(max_width / 2, max_height - 10,
                                     max_width - 10, max_height - 10, 300)
        except Exception as e:
            logging.error('error during unlock screen')
            raise e
            pass

    def construct_fastboot_command(self, command_parameter):
        lsPara = normalize_string_to_list(command_parameter)
        return 'fastboot -s %s %s' % (self.android_serial, ' '.join(lsPara))

    def construct_adb_command(self, command_parameter):
        lsPara = normalize_string_to_list(command_parameter)
        return 'adb -s %s %s' % (self.android_serial, ' '.join(lsPara))

    def send_command(self, commands):
        commands = normalize_string_to_list(commands)
        try:
            command_result = []
            for command in commands:
                logging.info('sending command %s' % command)
                command_result.append(
                    subprocess.getoutput(command)
                )
            pass
            return command_result
        except Exception as e:
            logging.error('dump the value of: command_result')
            logging.error(command_result)

            raise e
        else:
            pass

    def step_adb_getprop(self, sName):
        """
            to handle adb shell getprop
        """
        # return run('adb shell getprop %s' % (sName), timeout_sec=5)
        # return adb_session.run_cmd('shell getprop %s' % (sName))
        return self.send_command(
            self.construct_adb_command('shell getprop %s' % (sName))
        )

    def step_adb_root_shell(self, command):
        """
            send command by root shell (tinklabs1001)
            this is a workaround as tinklabs1001 -c {command} doesn't work

            :Args:
                - command - command would like to send by root shell
        """

        try:
            logging.debug('trying to send command as root %s' % command)
            adb_commands = []
            adb_commands.append((PATH_ANDROID_TINKLABS1001, ['#']))

            # NOTE: normally '#' is enough for this, the reason i adding the '\n' as the text to grep because it helps escape from the error/disconnect condition.
            # otherwise it will cause pexpect a failure and escape from loop.
            # NOTE: by adding '\n', the implementation destroy the functionality of the 'ADB settings xxx ', so i cancel the work. need to find another way.
            adb_commands.append((command, ['#']))

            spawn_adb_shell = "adb -s %s shell" % self.android_serial

            child = pexpect.spawn(
                spawn_adb_shell
            )

            index = child.expect(["$", "@", pexpect.TIMEOUT])

            for (command_to_send, text_expected) in adb_commands:
                logging.debug('sending %s' % command_to_send)
                send_command_to_adb(
                    child, command_to_send, text_expected
                )
            pass

        except Exception as e:

            logging.error('dump the value of: command')
            logging.error(command)

            logging.error('dump the value of: command_to_send')
            logging.error(command_to_send)

            logging.error('dump the value of: text_expected')
            logging.error(text_expected)

            raise e
        else:
            pass

    def ADB_PATH_ANDROID_TEMP_directory_is_ready(self, sSeconds):
        """
        check if the filesystem in android is ready

        Args:
            sSeconds: seconds until timeout
        """
        try:
            time_to_end = int(get_epoch_time()) + int(sSeconds)
            bDirectoryReady = False

            while time_to_end > int(get_epoch_time()):
                # (iReturnCode, sStdOut, sStdErr, bTimeout)=run('adb shell ls -l %s' % PATH_ANDROID_TEMP, timeout_sec=5)

                result = self.send_command(
                    self.construct_adb_command(
                        'shell ls -l %s' % PATH_ANDROID_TEMP
                    )
                )
                result = ''.join(result)

                # if iReturnCode == 0 :
                if result.find('No such file or directory') > -1:
                    logging.debug(
                        'STEP: directory not found, wait a while a re-check')
                    sleep(3)

                    pass
                else:
                    bDirectoryReady = True
                    break

            if bDirectoryReady:
                pass
            else:
                logging.debug('cannot get android temp direcotory')
                assert False
            pass
        except Exception as e:
            logging.error('error during getting directory')
            logging.error('dump the value of: PATH_ANDROID_TEMP')
            logging.error(PATH_ANDROID_TEMP)

            raise e
        else:
            pass

    def step_adb_change_permission(self, sTargetFile, sPermission):
        """to change the permission of file"""
        try:
            return self.send_command(
                self.construct_adb_command(
                    'shell "chmod %s %s"' % (sPermission, sTargetFile)
                )
            )

            pass
        except Exception as e:
            logging.error('error during change permission , %s %s ' %
                          (sPermission, sTargetFile))
            raise e
        else:
            pass
        pass

    def step_ADB_change_permission_tinklabs1001(self):
        """
        packed process to change the file permission of tinklabs1001
        """
        try:
            logging.debug('change permission of tinklabs1001')
            self.step_adb_change_permission(
                "777", dParameters['PATH_ANDROID_TINKLABS1001']
            )
            pass
        except Exception as e:
            logging.error('error during change permission tinklabs1001')
            raise e
        else:
            pass

    def step_push_to_android(self, sSourceFile, sTargetFile):
        """to handle file coping from PC to android
            TODO: obsolete

            "Args":
                - sSourceFile - Source file from PC
                - sTargetFile - Target file in android
        """
        # adb = context.adb_session
        # adb.push_local_file(sSourceFile, sTargetFile)

        # adb.run_cmd('push %s %s' %(sSourceFile, sTargetFile))
        # subprocess.check_output(
        #     'adb push %s %s' % (sSourceFile, sTargetFile)
        #     ,shell= True)

        # context.adb_session.run_cmd(
        #     'push %s %s' % (sSourceFile, sTargetFile)
        # )
        return self.send_command(
            self.construct_adb_command(
                'push %s %s' % (sSourceFile, sTargetFile)
            )
        )
        pass

    def step_adb_setting_put(self, sNamespace, sSettingName, sValue):
        """to handle the google application verification before test run
            :Args:
                - sValue - value of package_verifier_enable wanted
        """
        logging.debug('I am supposed to change the %s to %s' %
                      (sSettingName, sValue))

        # TODO: better implementation

        # context.execute_steps(u'''
        #     Then ADB shell ""source /data/local/tmp/change_settings.sh put %s %s %s""
        # ''' % (sNamespace, sSettingName, sValue))

        try:
            logging.debug('putting settings')
            # context.execute_steps(u'''
            #     Then adb root shell "settings put %s %s %s"
            # ''' % (sNamespace, sSettingName, sValue))

            self.step_adb_root_shell(
                "settings put %s %s %s" % (sNamespace, sSettingName, sValue)
            )

            pass
        except Exception as e:
            logging.error('error during putting settings')

            logging.error('dump the value of: sNamespace')
            logging.error(sNamespace)

            logging.error('dump the value of: sSettingName')
            logging.error(sSettingName)

            logging.error('dump the value of: sValue')
            logging.error(sValue)

            raise e
        else:
            pass

        pass

    def step_adb_push_thinkabs1001(self):
        """packed process to transfer the tinklabs1001 to android"""
        try:
            logging.debug('pushing tinklabs1001')
            # context.execute_steps(u'''
            #     Then ADB push "%(PATH_PC_TINKLABS1001)s" "%(PATH_ANDROID_TEMP)s"
            # ''' % dParameters)
            # pass
            self.step_push_to_android(
                dParameters['PATH_PC_TINKLABS1001'], dParameters['PATH_ANDROID_TEMP']
            )

        except Exception as e:
            logging.error('error during pushing tinklabs1001')
            raise e
        else:
            pass

    def fastboot_reboot(self):
        """perform fastboot reboot for the device"""
        try:
            self.lsCommand = []
            self.lsCommand.append(
                self.construct_fastboot_command('reboot'))
            result = self.send_command(
                self.lsCommand
            )
        except Exception as e:
            raise e

            logging.error('dump the value of: self.lsCommand')
            logging.error(self.lsCommand)

        else:
            pass

    def fastboot_erase_userdata(self):
        """stored procedure to erase user data by fastboot"""
        
        self.lsCommand = []

        try:
            if self.device_model == 'T1':

                self.lsCommand.append(
                    self.construct_fastboot_command('-i 0x489 oem fih on'))
                self.lsCommand.append(
                    self.construct_fastboot_command('-i 0x489 oem devlock key'))
                self.lsCommand.append(
                    self.construct_fastboot_command('-i 0x489 erase userdata'))
                self.lsCommand.append(
                    self.construct_fastboot_command('reboot'))

            elif self.device_model == 'M812':
                self.lsCommand.append(
                    self.construct_fastboot_command(' erase userdata'))
                self.lsCommand.append(
                    self.construct_fastboot_command('reboot'))
            else:
                logging.debug('not handled fastboot procedure , skipping')
                self.lsCommand.append(
                    self.construct_fastboot_command('reboot'))


            result = self.send_command(self.lsCommand)

        except Exception as e:
            logging.error('error during Fastboot Erase userdata')

            logging.error('dump the value of: result')
            logging.error(result)

        else:
            pass

    def adb_reboot_to_bootstrap(self):
        """adb reboot device to bootstrap mode"""
        try:
            logging.debug('STEP: adb reboot to bootstrap start')
            lsCommand = []
            lsCommand.append(
                self.construct_adb_command(
                    'reboot bootloader'
                ))
            result = self.send_command(lsCommand)
            logging.debug('STEP: adb reboot to bootstrap done')
        except Exception as e:

            logging.error('dump the value of: result')
            logging.error(result)

            raise e
        else:
            pass

    def adb_wait_for_device(self, seconds):
        """wrapper for adb wait-for-device"""
        try:
            logging.debug('STEP: adb wait-for-device start')
            time_to_start = get_epoch_time()
            lsCommand = []
            lsCommand.append(
                self.construct_adb_command(
                    'wait-for-device'
                ))
            self.send_command(lsCommand)

            # # (iRetrunCode, sStdOut, sStdErr, bTimeout) = result
            # context.time_poweron_to_adb_ready = get_time_difference_to(
            #     time_to_start)

            # # wait some seconds more to let device ready
            # sleep(3)
            logging.debug('STEP: adb wait-for-device done')
            pass
        except Exception as e:
            logging.error('error during adb waiting for device ready')
            raise e
        else:
            pass

    def adb_check_boot_completed(self, sSeconds):
        """
            to track the device status at fixed 15 seconds interval
            :Args:
                - sSeconds - timeout for the process
        """
        try:

            bBootComplete = False
            sStdOut = ''
            sStdErr = ''

            time_start = get_epoch_time()
            time_to_end = time_start + int(sSeconds)

            # for i in range(0, int(sSeconds)):
            while time_to_end > get_epoch_time():
                logging.debug('checkig for passing boot animation...')
                # (sResultCode, sStdOut, sStdErr, bTimeout) = step_adb_getprop(context, "sys.boot_completed")
                sStdOut = self.step_adb_getprop('sys.boot_completed')
                sStdOut = ''.join(sStdOut).strip()

                if sStdOut == '1':
                    bBootComplete = True
                    break
                else:
                    logging.debug('STEP: sleep before next check')
                    sleep(60)

            if bBootComplete:
                # context.time_sys_boot_animation = get_time_difference_to(
                #     time_start)
                logging.debug('sys.boot_completed received')
                logging.debug('ADB check boot complete done')
                pass
            else:
                logging.debug('boot failed')
                logging.debug('sStdOut: %s' % sStdOut)
                assert False, 'boot failed'

            pass
        except Exception as e:
            logging.error('error during ADB check boot completed')
            logging.error('dump the value of: sStdOut')
            logging.error(sStdOut)

            raise e
        else:
            pass

    def step_create_appium_session(self, port):
        try:
            logging.debug('setting up appium session')

            desired_caps = {}
            desired_caps['deviceName'] = 'Android'
            desired_caps['platformName'] = 'Android'

            # desired_caps['app'] = row['PATH(packageName)']
            desired_caps['appPackage'] = 'com.tinklabs.activateapp'
            desired_caps['appActivity'] = '.features.wizard.WizardActivity'
            # desired_caps['appWaitActivity'] = '.features.wizard.WizardActivity'

            desired_caps['deviceReadyTimeout'] = 30
            desired_caps['noReset'] = True

            desired_caps['udid'] = self.android_serial
            desired_caps['newCommandTimeout'] = 240


            desired_caps['automationName'] = 'UiAutomator2'
            desired_caps['skipUnlock'] = True

            self.appiumSession = webdriver.Remote(
                'http://localhost:%d/wd/hub' % int(port),
                desired_caps)

            sleep(3)

            logging.debug('setup appium done')

        except Exception as e:
            logging.error('cannot connect to the appium')
            logging.error('dump the value of: port')
            logging.error(port)

            raise e
        else:
            pass

    def step_create_appium_session_Launcher(self, port=4723):
        """create appium session and connect to it

        Args:
            port: appium port (default: 4723)
        """
        try:
            logging.debug('setting up appium session')

            desired_caps = {}
            desired_caps['deviceName'] = 'Android'
            desired_caps['platformName'] = 'Android'

            # desired_caps['app'] = row['PATH(packageName)']
            desired_caps['appPackage'] = 'com.tinklabs.launcher'
            desired_caps['appActivity'] = desired_caps['appPackage'] + \
                '.features.main.activity.LauncherActivity'
            # desired_caps['appWaitActivity'] = '.features.main.activity.LauncherActivity'

            desired_caps['deviceReadyTimeout'] = 30
            desired_caps['noReset'] = True

            desired_caps['udid'] = self.android_serial
            desired_caps['newCommandTimeout'] = 240

            # desired_caps['automationName'] = 'UiAutomator2'

            self.appiumSession = webdriver.Remote(
                'http://localhost:%d/wd/hub' % int(port),
                desired_caps)

            sleep(3)

            logging.debug('setup appium done')

        except Exception as e:
            logging.error('cannot connect to the appium')
            logging.error('dump the value of: port')
            logging.error(port)

            raise e
        else:
            pass

    def step_tap_on_position(self, sX, sY):
        """tap on specific position

        Args:
            sX, sY: coordinates of tap
        """

        # sTapCmd = "adb shell input tap %s %s" % (sX, sY)
        # lCmd = sTapCmd.split(' ')
        # subprocess.check_output(lCmd)
        try:
            logging.debug('STEP: tap on position')
            self.send_command(
                self.construct_adb_command(
                    'shell input tap %d %d' % (sX, sY)
                )
            )
            pass
        except Exception as e:
            logging.error(
                'error found during tapping screen to keep awake using adb')

            logging.error('dump the value of: sX')
            logging.error(sX)

            logging.error('dump the value of: sY')
            logging.error(sY)

            raise e
        else:
            pass

        pass

    def step_capture_english_on_screen(self, Text, TimeOut, interval):
        """Just wait the target Text appears, counted down by TimeOut seconds

        Args:
            Text: text to capture
        """

        try:
            #   tapElementByXpath

            TextFound = False
            start_time = get_epoch_time()
            end_time = start_time + int(TimeOut)

            while end_time > get_epoch_time():

                # STEP: try to locate English
                logging.info("STEP: try to locate English")
                els = self.selectElementsByXpath(
                    '//*[contains(@text, "English")]')

                if len(els) > 0:
                    TextFound = True
                    break
                else:
                    # STEP: sleep a while
                    logging.debug(
                        'STEP: sleep a while as wanted text not found')
                    sleep(interval)

                    # STEP: sending null tap
                    logging.info("STEP: sending null tap")
                    self.step_tap_on_position(10, 10)

            if not(TextFound):
                if appears in ['appears']:
                    assert False, "the wanted text doesn't appear"

        except Exception as e:
            logging.error("error as the wanted text doesn't appear")
            logging.error('dump the value of: TextFound')
            logging.error(TextFound)

            raise e
        else:
            pass

        pass

    def wizardActivityHappyFlow(self):
        """packed procedure to proceed happyflow in wizardActivity"""
        try:
            # STEP: tap the square at the bottom
            logging.info("STEP: tap the square at the bottom")

            self.tapElementByXpath(
                '//*[contains(@resource-id, "com.tinklabs.activateapp:id/tnc_checkbox")]',
                60, 1
            )
            # STEP: proceed to next page
            logging.info("STEP: proceed to next page")
            self.tapElementByXpath(
                '//*[contains(@resource-id, "com.tinklabs.activateapp:id/image_view_begin_btn")]',
                60, 1
            )

            # STEP: Checkout Calendar, Checkout Calendar Skippable
            logging.info(
                "STEP: Checkout Calendar, Checkout Calendar Skippable")
            self.tapElementByXpath(
                '//*[contains(@resource-id, "com.tinklabs.activateapp:id/tv_skip")]',
                60, 1
            )

            # STEP: handy Login, handy Login Skippable
            logging.info("STEP: handy Login, handy Login Skippable")
            self.tapElementByXpath(
                '//*[contains(@resource-id, "com.tinklabs.activateapp:id/tv_skip")]',
                60, 10
            )

            # STEP: personalized experience
            logging.info("STEP: personalized experience")
            self.tapElementByXpath(
                '//*[contains(@resource-id, "com.tinklabs.activateapp:id/tv_skip")]',
                60, 10
            )

            pass
        except Exception as e:
            logging.error('error during wizardActivityHappyFlow')
            raise e
        else:
            pass

    def waitForXpathAppears(self, xpath, timeout, check_interval):
        """wait for Xpath to appears in given time

        Args:
            xpath: xpath to capture
            timeout: timeout value to raise fail
            check_interval: check_inteval for the xpath
        """
        time_now = get_epoch_time()
        time_end = time_now + timeout
        try:
            # STEP: waiting fro xpath appears
            logging.info("STEP: waiting fro xpath appears")
            while time_end > get_epoch_time():
                els = self.selectElementsByXpath(xpath)
                if len(els) > 0:
                    # STEP: xpath found, escape from waiting loop
                    logging.info("STEP: xpath found, escape from waiting loop")

                    el_found = True
                    break
                else:
                    sleep(check_interval)
                    pass

            return el_found

            pass
        except Exception as e:
            logging.error('error during waitForXpathAppears')
            logging.error('dump the value of: xpath')
            logging.error(xpath)

            raise e
        else:
            pass
        el_found = False

    def tapElementByXpath(self, xpath, timeout, check_interval):
        """wait and tap for the elements

        Args:
            xpath: xpath to wait and tao
            timeout: time to raise error
            check_interval: checking interval
        """

        try:
            if self.waitForXpathAppears(xpath, timeout, check_interval):
                logging.debug('STEP: the xpath found')
                els = self.selectElementsByXpath(xpath)
                els[0].click()
            else:
                # STEP: cannot find the wanted xpath within timeout provided
                logging.info(
                    "STEP: cannot find the wanted xpath within timeout provided")
                raise 'Element wanted not found'
                pass
            pass
        except Exception as e:
            logging.error('dump the value of: xpath')
            logging.error(xpath)

            raise e
        else:
            pass

    def scrollSidemenu(self):
        """perfor scroll action on side menu"""
        try:
            logging.debug('STEP: scrollSidemenu start')
            els = self.selectElementsByXpath(
                '//*[contains(@resource-id, "com.tinklabs.launcher:id/title")]'
            )
            self.appiumSession.scroll(
                els[1], els[0]
            )
            logging.debug('STEP: scrollSidemenu done')
        except Exception as e:
            logging.debug('STEP: error during scrolling the sidemenu')
            raise e
        else:
            pass

    def scrollSidemenuToItem(self, item_wanted, maxium_try):
        """perform scroll until the wanted item appears on screen

        Args:
            item_wanted: the menu item wanted
            maximum_try: the maximum number of try to scroll
        """
        try:
            # STEP: scrollSidemenuToItem
            logging.info("STEP: scrollSidemenuToItem")

            item_found = False
            i = 0
            while not(item_found) and i < maxium_try:
                i += 1
                els = self.selectElementsByXpath(
                    '//*[@text="%s"]' % item_wanted
                )
                if len(els) > 0:
                    item_found = True
                    break
                else:
                    # STEP: item not found, scroll
                    logging.info("STEP: item not found, scroll ")
                    self.scrollSidemenu()

            pass
        except Exception as e:
            logging.debug(
                'error occur during scrollSidemenuToItem', 'Fail')

            raise e

        pass

    def selectElementsByXpath(self, xpath):
        """select element by xpath

        Args:
            xpath: xpath

        Returns:
            els: elements in array selected by xpath

        """
        try:
            els = self.appiumSession.find_elements_by_xpath(
                xpath
            )
            return els
            pass
        except Exception as e:
            logging.error('error occur during selectElesmentsByXpath', 'Fail')
            self.screencapture()
            raise e

        pass

    def first_time_launcher_tutorial(self):
        """packed action to perform first time tutorial in launcher"""
        try:
            logging.debug('STEP: first time launcher tutorial start')
            # STEP: Tap this show the hotel details.
            logging.info("STEP: Tap this show the hotel details.")
            self.tapElementByXpath(
                '//*[contains(@text, "Tap this show the hotel details.")]',
                30, 3
            )

            # STEP: Shop for discounted souvenirs and the hottest new products, and enjoy free delivery.
            logging.info(
                "STEP: Shop for discounted souvenirs and the hottest new products, and enjoy free delivery.")
            self.tapElementByXpath(
                '//*[contains(@text, "Shop for discounted souvenirs and the hottest new products, and enjoy free delivery.")]',
                30, 3
            )

            # STEP: Tours and tickets to major attractions - all available here at a discount.
            logging.info(
                "STEP: Tours and tickets to major attractions - all available here at a discount.")
            self.waitForXpathAppears(
                '//*[contains(@text, "Tours and tickets to major attractions - all available here at a discount.")]',
                30, 3
            )

            self.tapElementByXpath(
                '//*[contains(@text, "Tickets")]', 30, 3)

            # STEP: after clicking, the page showup
            logging.info("STEP: after clicking, the page showup")
            self.waitForXpathAppears(
                '//*[@class="android.widget.TextView" and @text="Tickets"]',
                30, 3
            )
            self.waitForXpathAppears(
                '//*[@class="android.widget.ImageButton" and @clickable="true"]',
                30, 3
            )
            self.tapElementByXpath(
                '//*[@class="android.widget.ImageButton" and @clickable="true"]',
                30, 3
            )

            logging.debug('STEP: first time launcher tutorial done')
            pass
        except Exception as e:
            logging.error(
                'error occur during first_time_launcher_tutorial', 'Fail')

            raise e

        pass

    def step_press_button(self, ButtonName):
        try:
            logging.debug('STEP: press button start')
            if ButtonName == 'HOME':
                finger.f_PressKey(self.appiumSession,
                                  android_key_const.HOME)
            pass
        except Exception as e:
            logging.error('error pressing button')

            logging.error('dump the value of: ButtonName')
            logging.error(ButtonName)
            self.screencapture()

            raise e
        else:
            pass

    def EraseDataFromDevice(self):
        """packed action to erase data from device"""
        self.clickEraseFromMenu()
        self.clickEraseDataInEraseDataPage()
        self.confirmEraseDataDialog()

    def clickHamburgerButton(self):
        try:
            # STEP: clickHamburgerButton
            logging.info("STEP: clickHamburgerButton")

            self.tapElementByXpath(
                '//*[contains(@resource-id,"com.tinklabs.launcher:id/menu_button")]', 30, 5
            )

            pass
        except Exception as e:
            logging.debug('error occur during clickHamburgerButton', 'Fail')
            self.screencapture()
            raise e

        pass

    def clickEraseDataFromSidemenu(self):
        try:
            # STEP: find erase data from sidemenu
            logging.info("STEP: find erase data from sidemenu")
            self.scrollSidemenuToItem(
                'Erase Data', 10
            )

            self.tapElementByXpath(
                '//*[@text="Erase Data"]/ancestor::*[@clickable="true"]', 30, 1
            )

            # STEP: clickEraseDataFromSidemenu
            logging.info("STEP: clickEraseDataFromSidemenu")

            pass
        except Exception as e:
            logging.debug(
                'error occur during clickEraseDataFromSidemenu', 'Fail')
            self.screencapture()
            raise e

        pass

    def clickEraseFromMenu(self):
        """packed action to click Erase Data from side menu"""
        try:
            # STEP: clickEraseFromMenu
            logging.info("STEP: clickEraseFromMenu")

            self.clickHamburgerButton()
            self.clickEraseDataFromSidemenu()

            pass
        except Exception as e:
            logging.debug('error occur during clickEraseFromMenu', 'Fail')

            raise e

        pass

    def waitForEraseDataPage(self):
        try:
            # STEP: waitForEraseDataPage
            logging.info("STEP: waitForEraseDataPage")

            self.waitForXpathAppears(
                '//*[contains(@text, "Erase Data") and @resource-id="com.tinklabs.activateapp:id/title"]',
                60, 5
            )

            pass
        except Exception as e:
            logging.debug(
                'error occur during waitForEraseDataPage', 'Fail')
            self.screencapture()
            raise e

        pass

    def clickEraseDataInEraseDataPage(self):
        """packed action to click ERASE DATA button in erase data pgae"""
        try:
            # STEP: clickEraseDataInEraseDataPage
            logging.info("STEP: clickEraseDataInEraseDataPage")
            self.waitForEraseDataPage()
            self.tapElementByXpath(
                '//*[contains(@resource-id,"com.tinklabs.activateapp:id/mira_factory_reset")]',
                60, 5
            )

            pass
        except Exception as e:
            logging.debug(
                'error occur during clickEraseDataInEraseDataPage', 'Fail')
            self.screencapture()
            raise e

        pass

    def confirmEraseDataDialog(self):
        """packed action to perform clicking YES to the confirmation dialog"""
        try:
            # STEP: confirmEraseDataDialog
            logging.info("STEP: confirmEraseDataDialog")
            self.waitForConfirmationDialog('Confirmation')

            self.tapElementByXpath(
                '//*[@resource-id="android:id/button1"]',
                60, 5
            )

            pass
        except Exception as e:
            logging.debug(
                'error occur during confirmEraseDataDialog', 'Fail')
            self.screencapture()
            raise e

        pass

    def waitForConfirmationDialog(self, dialog_title):
        """packed procedure for waiting confirmation dialog appears"""
        try:
            # STEP: waitForConfirmationDialog
            logging.info("STEP: waitForConfirmationDialog")
            self.waitForXpathAppears(
                '//*[contains(@resource-id,"android:id/alertTitle") and @text="Confirmation"]',
                60, 5
            )

            pass
        except Exception as e:
            logging.debug(
                'error occur during waitForConfirmationDialog', 'Fail')
            self.screencapture()
            raise e

        pass


def bootstrap_from_unknown_state(android_serial):
    """ for handle the device at the very beginnibng
        I would like to make the device printable from "adb devices" while escape from this loop

    Args:
        android_serial: the serial number of android

    NOTES/IDEAS:
        to guide the device incase the device is trapped into the fastboot mode.
    """

    keep_loop = True
    countdown = 10

    try:
        while keep_loop and countdown > 0:
            logging.debug('countdown remains for bootstrap :%d' % countdown)
            countdown -= 1
            sleep(1)

            adb_devices_output = subprocess.check_output(['adb', 'devices'])
            adb_devices_output = str(adb_devices_output)

            if adb_devices_output.find(android_serial) > -1:
                # if the device serial is found from adb devices output, escape from the loop
                logging.debug('device appears in the adb devices result')
                keep_loop = False
                pass
            else:
                # if the device serial cannot found from adb devices output
                # possibly the device is in the bootloader mode, fastboot -> reboot the device to recover
                logging.debug('device not appears in the adb devices result')

                logging.debug('dump the value of: adb_devices_output')
                logging.debug(adb_devices_output)

                fastboot_output = subprocess.check_output(
                    ['fastboot', 'devices'])
                if fastboot_output.find(android_serial) > -1:
                    logging.debug(
                        'devices appears in the fastboot devices result')
                    subprocess.check_output(
                        ['fastboot', '-s', android_serial, 'reboot'])
                    sleep(90)
                else:
                    logging.debug(
                        'devices not appears int the fastboot devices result')
                    logging.error('dump the value of: fastboot_output')
                    logging.error(fastboot_output)

        pass
    except Exception as e:
        logging.error('error found during bootstrap from unknown state')
        logging.error('is the android_serial number correct ?')

        logging.error('dump the value of: adb_devices_output')
        logging.error(adb_devices_output)
        logging.error('dump the value of: android_serial')
        logging.error(android_serial)

        logging.error('dump the value of: fastboot_output')
        logging.error(fastboot_output)

        raise e
    else:
        pass


# @step(u'ADB Reboot bootloader')
def ADB_reboot_bootloader(context):
    """reboot the android by adb command adb reboot"""
    if hasattr(context, 'adb_session'):
        pass
    else:
        assert False, "adb_session not found"

    # adb = context.adb_session
    # adb.run_cmd('reboot bootloader')
    adb_reboot_command = 'adb -s %s reboot bootloader' % context.android_serial

    logging.debug('dump the value of: adb_reboot_command')
    logging.debug(adb_reboot_command)

    subprocess.check_output(adb_reboot_command.split(' '))
    sleep(5)


# @step(u'Fastboot init')
def fastboot_init(context):
    """
    To initialize fastboot session
    implict reboot by adb occur.
    """
    try:
        if hasattr(context, 'android_serial'):
            sleep(3)
            logging.debug('android_serial:%s is used for fastboot')

            logging.debug('reboot device by adb')
            context.execute_steps(u'''
                Then ADB Reboot bootloader
            ''')

            # NOTE: this is a small technique for using the fastboot library.
            # the get_devices also update the list inside the library.
            f_session = context.fastboot_session

            f_session.set_target_by_id(
                get_index_by_serial(f_session.get_devices(),
                                    context.android_serial)
            )
        else:
            # NOTE: no android_serial info here. assert error
            logging.error('android_serial not found')
            assert False, 'android_serial not found'

    except Exception as e:
        logging.error('error during Fastboot init')
        raise e
    else:
        pass


def send_command_to_adb(adb_shell_process, command_to_send, texts_expected):
    """send command to adb shell and wait for ready
    Args:
        adb_shell_process - the process given by spawn (pexpect -> adb)
        command_to_send - command i would like to send to the adb
        texts_expected - list if text i am expecting
    """
    try:

        # TODO: normalize the texts_expected accept single string as input

        logging.debug('dumping the value of command_to_send')
        logging.debug(command_to_send)

        # NOTE: construct the send process by command and timeout
        adb_shell_process.sendline(command_to_send)
        texts_expected.append(pexpect.TIMEOUT)

        return adb_shell_process.expect(texts_expected)

    except Exception as e:
        logging.error('error during sending command to adb')
        logging.error(command_to_send)
        raise e
    else:
        pass
