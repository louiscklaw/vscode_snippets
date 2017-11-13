from apscheduler.schedulers.blocking import BlockingScheduler
import os
import sys
import datetime
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datafmt='%a, %d %b %Y %H:%M:%S',
                    filename='%s' % __file__.replace('.py', '.log'),
                    filemode='a')

from scheduler_lib import *

import subprocess

PROJ_HOME = os.path.dirname(os.path.abspath(__file__))
RESULT_DIRECTORY = os.path.sep.join(
    [PROJ_HOME, './result'])

APPIUM_BINARY = r'/usr/local/bin/appium'


def schedulerM812():
    try:
        # NOTE: test configuration
        android_serial_M812 = 'V2HGLMB721301100'

        if checkAndroidBatteryLevel(android_serial_M812, 50):
            # STEP: battery level OK
            logging.debug("STEP: battery level OK")

            time.sleep(10)

            # STEP: start the test
            logging.debug("STEP: start the test")
            command_to_start_test = unittestCommandConstructor(
                'random_click_M812.py',
                os.path.sep.join(
                    [RESULT_DIRECTORY, 'M812', gettestLogFilename()])
            )

            logging.debug(command_to_start_test)
            osCommand(command_to_start_test)
        else:
            # STEP: battery level too low, skipping
            logging.debug("STEP: battery level too low, skipping this run")

    except Exception as e:
        logging.error('error occur at the scheduler M812')
        logging.error('android device %s ' % android_serial_M812)
        logging.error('battery level%s ' % getBatteryInfo(android_serial_M812))

        logging.error('dump the value of: android_serial_M812')
        logging.error(android_serial_M812)
        logging.error('dump the value of: command_to_start_test')
        logging.error(command_to_start_test)

        raise e
    else:
        pass



scheduler = BlockingScheduler()
#scheduler.add_job(schedulerT1, 'cron',
#                  minute='*/5')
scheduler.add_job(schedulerM812, 'cron',
                  minute='*/30',
                  max_instances=2)
# schedulerT1()
scheduler.start()
