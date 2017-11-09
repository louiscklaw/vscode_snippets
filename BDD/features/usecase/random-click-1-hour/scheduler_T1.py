from apscheduler.schedulers.blocking import BlockingScheduler
import os, sys
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



def schedulerT1():
    try:
        # STEP: kill old appium if possible
        logging.debug("STEP: kill old appium if possible")
        android_serial_T1 = 'VZHGLMA742804186'

        kill_if_appium_process_exist(android_serial_T1, 10)

        # STEP: start appium process
        logging.debug("STEP: start appium process")
        startAppiumProcess(
            android_serial_T1,
            '4723',
            '4724',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'T1', getAppiumLogFilename()])
        )

        time.sleep(10)

        # STEP: start the test
        logging.debug("STEP: start the test")
        command_to_start_test = behaveCommandConstructor(
            'random-click-1-hour_T1.feature',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'T1', gettestLogFilename()])
        )

        logging.debug(command_to_start_test)
        osCommand(command_to_start_test)
    except Exception as e:
        logging.error('error occur at the scheduler T1')

        # TODO: consider remove me
        from pprint import pprint
        logging.error('dump the value of: android_serial_T1')
        pprint(android_serial_T1)
        logging.error('dump the value of: command_to_start_test')
        pprint(command_to_start_test)

        raise e
    else:
        pass


scheduler = BlockingScheduler()
scheduler.add_job(schedulerT1, 'cron',
                  minute='*/15')
#scheduler.add_job(schedulerM812, 'cron',
#                  minute='*/5')
# scheduler.start()
# schedulerT1()
scheduler.start()
