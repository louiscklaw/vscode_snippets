import os, sys

import unittest
import scheduler_lib

from pprint import pprint

import logging



logging.basicConfig(level=logging.DEBUG,
   format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
   datefmt='%a, %d %b %Y %H:%M:%S',
   filename='%s' % __file__.replace('.py', '.log'),
   filemode='a')



class Test_getPidOfProcess(unittest.TestCase):

    def setUp(self):
        self.ANDROID_SERIAL = 'VZHGLMA742901014'
        pass

    def tearDown(self):
        pass

    def failIfNotInt(self, guess):
        self.assertTrue(type(1) == type(guess))

    def failIfNotList(self, guess):
        self.assertTrue(type([]) == type(guess))

    def test_grep_process_single(self):
        pid = scheduler_lib.getPidOfProcess('ps -ef')
        print(pid)
        self.failIfNotList(pid)

    def test_grep_process_multi(self):
        pid = scheduler_lib.getPidOfProcess(['ps -ef','ps -ef'])
        print(pid)
        self.failIfNotList(pid)


    def test_grep_process_not_exist(self):
        pid = scheduler_lib.getPidOfProcess(['notexist', 'not exist'])
        print(pid)
        self.failIfNotList(pid)


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_getBatteryInfo(self):
        """check for getting the battery level from android"""
        # TODO: Temporary solution ...
        print("'%s'" % scheduler_lib.getBatteryInfo(self.ANDROID_SERIAL))

    def test_checkAndroidBatteryLevelIsAboveThreshold(self):
        self.assertTrue(scheduler_lib.checkAndroidBatteryLevel(self.ANDROID_SERIAL, 1))

    def test_checkAndroidBatteryLevelIsBelowThreshold(self):
        self.assertFalse(scheduler_lib.checkAndroidBatteryLevel(
            self.ANDROID_SERIAL, 101))

if __name__ == '__main__':
    unittest.main()
