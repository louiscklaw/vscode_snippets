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

import subprocess

from random_click_lib import *


class TestStringMethods(unittest.TestCase):
    android_serial = 'VZHGLMA742800785'

    def setUp(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def tearDown(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_check_grepping_serial(self):
        adb_devices_output = subprocess.check_output(['adb', 'devices'])
        adb_devices_output = str(adb_devices_output)
        self.assertTrue(adb_devices_output.find(self.android_serial))

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_setup_fastboot(self):
        handy_command_session = handy_command(
            'T1',
            'VZHGLMA742800785')
        handy_command_session.fastboot_erase_userdata()

    def test_send_command_adb(self):
        handy_command_session = handy_command(
            'T1',
            'VZHGLMA742800785')

        test_result = handy_command_session.send_command(
            'adb devices'
        )

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: test_result')
        pprint(test_result)

    def test_send_command_fastboot(self):
        try:
            handy_command_session = handy_command(
                'T1',
                'VZHGLMA742800785')

            test_result = handy_command_session.send_command(
                'fastboot --version'
            )

            self.assertTrue(
                test_result == ['fastboot version 3db08f2c6889-android\nInstalled as /bin/fastboot'])
            pass
        except Exception as e:

            # TODO: consider remove me
            from pprint import pprint
            print('dump the value of: test_result')
            pprint(test_result)

            raise e
        else:
            pass

    def test_step_adb_setting_put(self):
        print('putting settings')
        sNamespace = 'global'
        sSettingName = 'package_verifier_enable'
        sValue = '0'

        handy_command_session = handy_command(
            self.test_setup.device,
            self.test_setup.android_serial)

        handy_command_session.step_adb_root_shell(
            "settings put %s %s %s" % (sNamespace, sSettingName, sValue)
        )


if __name__ == '__main__':
    unittest.main()
