#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

from datetime import datetime


import unittest
from time import sleep


from scheduler_lib import *
from common_lib import *
from random_click_lib import *


PROJ_HOME = os.path.dirname(os.path.abspath(__file__))
RESULT_DIRECTORY = os.path.sep.join(
    [PROJ_HOME, './result'])

APPIUM_BINARY = r'/usr/local/bin/appium'


class test_setup:
    """dummy class for collecting test setup information"""
    pass


class TestStringMethods(unittest.TestCase):
    android_serial_M812 = 'V2HGLMB721301100'
    result_directory_M812 = os.path.sep.join(
        [RESULT_DIRECTORY, 'M812']
    )

    def setUp(self):
        try:
            self.DEBUG = os.getenv('DEBUG', 'N')

            setup_logging(self.result_directory_M812)
            logging.info('setup logging done')

            # STEP: kill old appium if possible
            logging.info("STEP: kill old appium if possible")

            # STEP: battery level OK
            logging.debug("STEP: battery level OK")

            # STEP: kill old appium if possible
            logging.debug("STEP: kill old appium if possible")
            kill_if_appium_process_exist(self.android_serial_M812, 10)

            # # STEP: kill old adb if possible
            # logging.info("STEP: kill old adb if possible")
            # kill_if_adb_process_exist()

            # STEP: start appium process
            logging.debug("STEP: start appium process")
            startAppiumProcess(
                self.android_serial_M812,
                '4725',
                '4726',
                os.path.sep.join(
                    [self.result_directory_M812, getAppiumLogFilename()])
            )

            self.SCREENCAPTURE_DIRECTORY = os.path.sep.join(
                [RESULT_DIRECTORY, 'M812', './_screencapture']
            )

            time.sleep(10)

        except Exception as e:
            logging.error('error occur at the setUp')
            raise e
        else:
            pass

        test_setup.device = "M812"
        test_setup.android_serial = self.android_serial_M812
        self.test_setup = test_setup

    def tearDown(self):
        # STEP: kill old appium if possible
        # logging.debug("STEP: kill old appium if possible")
        # kill_if_appium_process_exist(self.android_serial_M812, 10)

        pass

    def test_random_click(self):

        def erase_device():
            try:
                logging.debug('STEP: erase device start')
                handy_command_session.adb_reboot_to_bootstrap()
                handy_command_session.fastboot_erase_userdata()
                logging.info('STEP: erase device done')
                pass
            except Exception as e:
                logging.error('STEP: error during erasing device')
                handy_command_session.screencapture()
                raise e
            else:
                pass

        def prepare_device():
            try:
                logging.debug('STEP: perpare device start')
                logging.debug('STEP: waiting device power up->boot-complete')
                handy_command_session.adb_wait_for_device(900)
                handy_command_session.adb_check_boot_completed(900)

                logging.debug('STEP: bootstrap device')
                handy_command_session.ADB_PATH_ANDROID_TEMP_directory_is_ready(
                    600)
                handy_command_session.step_adb_push_thinkabs1001()
                handy_command_session.step_ADB_change_permission_tinklabs1001()

                # STEP: sleep some time for apps stablize
                logging.info("STEP: sleep some time for apps stablize")
                sleep(180)

                logging.debug(
                    'STEP: disable google application install dialog')
                handy_command_session.step_adb_setting_put(
                    "global", "package_verifier_enable", "0"
                )

                # STEP: try to inject unlock-debug.apk
                logging.debug("STEP: try to inject unlock-debug.apk")
                handy_command_session.unlockScreenHelper()

                logging.info('STEP: prepare device done')
                pass
            except Exception as e:
                logging.error('STEP: error during prepare device')
                handy_command_session.screencapture()
                raise e
            else:
                pass

        try:
            logging.info('STEP: test start')
            handy_command_session = handy_command(
                self.test_setup.device,
                self.test_setup.android_serial,
                self.result_directory_M812
            )

            erase_device()
            prepare_device()

            logging.debug('STEP: starting appium')
            handy_command_session.step_create_appium_session(
                4725,
                8002
            )

            logging.debug('STEP: waiting for "English" appears on screen')
            # wizardActivity, happyflow
            handy_command_session.step_capture_english_on_screen(
                "English", 300, 10
            )

            logging.debug('STEP: proceeding wizardActivity happyflow')
            # start the happyflow
            handy_command_session.wizardActivityHappyFlow()

            # STEP: landing launcher here
            logging.debug("STEP: landing launcher here")
            # STEP: launcher first time tutorial
            logging.debug("STEP: launcher first time tutorial")
            handy_command_session.first_time_launcher_tutorial()

            # STEP: suppose i random click here
            logging.debug("STEP: suppose i random click here")

            logging.debug('STEP: in launcher menu, erase data')
            handy_command_session.EraseDataFromDevice()

            logging.info('STEP: sleep some time for device reboot')
            sleep(180)

            logging.debug(
                'STEP: check that the English still appears after the device restart')

            logging.debug('STEP: re-prepare the device')
            prepare_device()

            logging.debug('STEP: starting appium')
            handy_command_session.step_create_appium_session(
                4725,
                8002
            )

            handy_command_session.step_capture_english_on_screen(
                "English", 300, 10
            )

            logging.info('STEP: test done, clear exit, RESULT: PASSED')
        except Exception as e:
            logging.error('STEP: test done, RESULT: FAILED')
            logging.error('error during running the test')

            handy_command_session.screencapture()
            self.assertTrue(
                'False', 'test failed as interrupted, RESULT: FAILED')

            raise e
        else:
            pass


if __name__ == '__main__':
    unittest.main()
