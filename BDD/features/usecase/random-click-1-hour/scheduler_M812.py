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

APPIUM_BINARY = r'/usr/local/bin/appium'




def schedulerM812():
    try:
        # STEP: kill old appium if possible
        print("STEP: kill old appium if possible")
        android_serial_M812 = 'V2HGLMB721301100'

        kill_if_appium_process_exist(android_serial_M812, 10)

        # STEP: start appium process
        print("STEP: start appium process")
        startAppiumProcess(
            android_serial_M812,
            '4725',
            '4726',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'M812', getAppiumLogFilename()])
        )

        time.sleep(10)

        # STEP: start the test
        print("STEP: start the test")
        command_to_start_test = behaveCommandConstructor(
            'random-click-1-hour_M812.feature',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'M812', gettestLogFilename()])
        )

        print(command_to_start_test)
        osCommand(command_to_start_test)
    except Exception as e:
        print('error occur at the scheduler M812')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: android_serial_M812')
        pprint(android_serial_M812)
        print('dump the value of: command_to_start_test')
        pprint(command_to_start_test)

        raise e
    else:
        pass


# def dial_Sender():
#     print(str(time.strftime("%Y%m%d-%H%M%S")) + " Start to execute Dail a Call")
#     osCommand('python handyCall_Dial_Sender.py')


# def dial_Receiver():
#     # print("aaa")
#     osCommand('python handyCall_Dial_Receiver.py')


# def VE_Sender():
#     print(str(time.strftime("%Y%m%d-%H%M%S")) + " Start to execute VE Call")
#     osCommand("python handyCall_VE_Sender.py")


# def VE_Receiver():
#     osCommand("python handyCall_VE_Receiver.py")


# def jobRecord():
#     print(datetime.datetime.time(datetime.datetime.now()))

#schedulerT1()

scheduler = BlockingScheduler()
#scheduler.add_job(schedulerT1, 'cron',
#                  minute='*/5')
scheduler.add_job(schedulerM812, 'cron',
                  minute='*/20')
# scheduler.start()
# schedulerT1()
scheduler.start()
