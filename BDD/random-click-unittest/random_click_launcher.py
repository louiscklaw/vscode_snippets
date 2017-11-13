#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='%s' % __file__.replace('.py', '.log'),
                    filemode='a')

import unittest
from time import sleep
# from pyadb import ADB, Fastboot


from scheduler_lib import *


# test specific configuratin
from random_click_lib import *


PROJ_HOME = os.path.dirname(os.path.abspath(__file__))
RESULT_DIRECTORY = os.path.sep.join(
    [PROJ_HOME, './result'])

APPIUM_BINARY = r'/usr/local/bin/appium'


class test_setup():
    pass


class TestStringMethods(unittest.TestCase):
    android_serial_T1 = 'VZHGLMA742800785'

    def setUp(self):
        try:
            # STEP: kill old appium if possible
            logging.info("STEP: kill old appium if possible")

            # STEP: battery level OK
            logging.info("STEP: battery level OK")

            # STEP: kill old appium if possible
            logging.info("STEP: kill old appium if possible")
            kill_if_appium_process_exist(self.android_serial_T1, 10)

            # STEP: start appium process
            logging.info("STEP: start appium process")
            startAppiumProcess(
                self.android_serial_T1,
                '4723',
                '4724',
                os.path.sep.join(
                    [RESULT_DIRECTORY, 'T1', getAppiumLogFilename()])
            )

            time.sleep(10)

        except Exception as e:
            print('error occur at the setUp')
            raise e
        else:
            pass

        test_setup.device = "T1"
        test_setup.android_serial = self.android_serial_T1
        self.test_setup = test_setup

    def tearDown(self):
        # STEP: kill old appium if possible
        # logging.info("STEP: kill old appium if possible")
        # kill_if_appium_process_exist(self.android_serial_T1, 10)

        pass

    def test_random_click(self):
        def erase_device():
            handy_command_session.adb_reboot_to_bootstrap()
            handy_command_session.fastboot_erase_userdata()

        def prepare_device():
            handy_command_session.adb_wait_for_device(600)
            handy_command_session.adb_check_boot_completed(600)

            handy_command_session.ADB_PATH_ANDROID_TEMP_directory_is_ready(600)
            handy_command_session.step_adb_push_thinkabs1001()
            handy_command_session.step_ADB_change_permission_tinklabs1001()

            sleep(18)
            handy_command_session.step_adb_setting_put(
                "global", "package_verifier_enable", "0"
            )

        try:

            setup_target_device(
                self.test_setup.device,
                self.test_setup.android_serial
            )

            handy_command_session = handy_command(
                self.test_setup.device,
                self.test_setup.android_serial,
                RESULT_DIRECTORY
            )

            # STEP: landing launcher here
            logging.info("STEP: landing launcher here")
            handy_command_session.step_create_appium_session_Launcher(
                4723
            )
            # STEP: unlocking screen
            logging.info("STEP: unlocking screen")

            handy_command_session.unLockScreen()
            # STEP: screen unlock done
            logging.info("STEP: screen unlock done")

            # STEP: launcher first time tutorial
            # logging.info("STEP: launcher first time tutorial")
            # handy_command_session.first_time_launcher_tutorial()

            # STEP: suppose i random click here
            logging.info("STEP: suppose i random click here")

            logging.debug('STEP: in launcher menu, erase data')
            handy_command_session.EraseDataFromDevice()

            # logging.debug(
            #     'STEP: check that the English still appears after the device restart')

            # prepare_device()

        except Exception as e:
            logging.debug('STEP: error during running the test')
            handy_command_session.screencapture()
            raise e
        else:
            pass

        # logging.debug('STEP: starting appium')
        # handy_command_session.step_create_appium_session(
        #     4723
        # )

        # handy_command_session.step_capture_english_on_screen(
        #     "English", 300, 10
        # )

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    unittest.main()
