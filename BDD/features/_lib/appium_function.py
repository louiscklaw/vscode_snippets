#!/usr/bin/env python
# coding:utf-8
import os, sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG,
   format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
   datefmt='%a, %d %b %Y %H:%M:%S',
   filename='debug.log',
   filemode='a')

from datetime import datetime


class appium_screen_capture:
    def __init__(self, appium_driver,screen_capture_directory):
        self.screen_capture_directory = screen_capture_directory
        self.appium_driver = appium_driver

    def capture_failed_screen(self):
        try:
            failed_screenshot_filename = 'failed_' + datetime.now().strftime('%y%m%d-%H%M%S')+'.png'
            self.screen_capture( self.screen_capture_directory, failed_screenshot_filename)
            print('screen capture saved to file: %s' % failed_screenshot_filename)
            pass
        except Exception as e:
            print('error during capture the screen')

            # TODO: consider remove me
            from pprint import pprint
            print('dump the value of: failed_screenshot_filenames')
            pprint(failed_screenshot_filename)

            raise e
        else:
            pass
        return self

    def screen_capture(self, directory, file_name):
        """simple facility to provide screen capture
            TODO: generalize me
        """
        appium_driver = ''

        try:
            appium_driver = self.appium_driver

            path_to_save_screenshot = os.path.sep.join([directory, file_name])
            print(path_to_save_screenshot)
            appium_driver.save_screenshot(path_to_save_screenshot)
            pass
        except Exception as e:

            # TODO: remove me
            from pprint import pprint
            print('dump the value of: appium_driver')
            pprint(appium_driver)

            print('dump the value of: file_name')
            pprint(file_name)

            print('dump the value of: path_to_save_screenshot')
            pprint(path_to_save_screenshot)

            raise e
        else:
            pass



