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

import scheduler_lib

import subprocess

PROJ_HOME = os.path.dirname(os.path.abspath(__file__))
RESULT_DIRECTORY = os.path.sep.join(
    [PROJ_HOME, './result'])

APPIUM_BINARY = r'/usr/local/bin/appium'


def osCommand(cmd):
    pyVesion = str(sys.version_info)
    if 'major=2' in pyVesion:
        import commands
        return commands.getoutput(cmd)
    else:
        import subprocess
        return subprocess.getoutput(cmd)


def getTodayString(offset=0):
    """get the day string using the format "yymmdd-hhmmss" with the given offset(default=0, +ve number for the day in the past)

    Args:
        offset : offset by days, 1 for yesterday, 2 for day before yesterday and so on...

    Returns:
        Return1 : the 1st arguments
    """
    t = datetime.datetime.now()
    return (t - datetime.timedelta(days=offset)).strftime('%d%m%Y-%H%M%S')


def getLogFileName(suffix):
    """generate a log file name only

    Args:
        appendix: the .3 format of the filename

    Returns:
        a filename with date string and suffix
    """
    print(getTodayString() + suffix)
    return getTodayString() + suffix


def getAppiumLogFilename():
    return getLogFileName('-appium.log')


def gettestLogFilename():
    return getLogFileName('-test.log')


def behaveCommandConstructor(feature_file, result_pipe_to_file):
    return 'behave -vk --no-capture  %s | tee %s' % (feature_file, result_pipe_to_file)


def getAppiumProcessPid(android_serial):
    """get the target appium by the android_serial attached"""
    return scheduler_lib.getPidOfProcess(['appium', android_serial])


def killAppiumProcess(appium_pid):
    return subprocess.call('kill %s' % appium_pid, shell=True)


def createAppiumCommand(android_serial, appium_port, appium_bootstrap_port):
    """to create the launchline for appium command

    Args:
        android_serial: the target android
        appium_port: the port appium listen on for commands
        appium_bootstrap_port: the port appium talk to the android

    Returns:
        Return1 : the pid of the appium
    """

    param = []
    param.append(APPIUM_BINARY)
    param.append(" ".join(["-U", android_serial]))
    param.append(" ".join(["-p", appium_port]))
    param.append(" ".join(['-bp', appium_bootstrap_port]))
    return ' '.join(param)

def startAppiumProcess(android_serial, appium_port, appium_bootstrap_port, appium_log):
    try:
        appium_command = createAppiumCommand(
            android_serial,
            appium_port,
            appium_bootstrap_port
        ) + ' > %s ' % appium_log
        p = subprocess.Popen(
            appium_command,
            shell=True
        )
        print(appium_command)
        return p
    except Exception as e:
        print('error during create appiumprocess')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: appium_command')
        pprint(appium_command)

        print('dump the value of: p.pid')
        pprint(p.pid)

        raise e
    else:
        pass
    return p.pid

def schedulerT1():
    try:
        # STEP: kill old appium if possible
        print("STEP: kill old appium if possible")
        android_serial_T1 = 'VZHGLMA742804186'

        appium_pid = getAppiumProcessPid(android_serial_T1)
        if appium_pid != -1 :
            killAppiumProcess(appium_pid)

        # STEP: start appium process
        print("STEP: start appium process")
        startAppiumProcess(
            android_serial_T1,
            '4723',
            '4724',
            os.path.sep.join([RESULT_DIRECTORY, 'T1', getAppiumLogFilename()])
        )

        # STEP: start the test
        print("STEP: start the test")
        command_to_start_test = behaveCommandConstructor(
            'random-click-1-hour_T1.feature',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'T1', gettestLogFilename()])
        )
        print(command_to_start_test)
        osCommand(command_to_start_test)
    except Exception as e:
        print('error occur at the scheduler T1')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: appium_pid')
        pprint(appium_pid)
        print('dump the value of: android_serial_T1')
        pprint(android_serial_T1)
        print('dump the value of: command_to_start_test')
        pprint(command_to_start_test)

        raise e
    else:
        pass


def schedulerM812():
    try:
        command_to_start_test = behaveCommandConstructor(
            'random-click-1-hour_M812.feature',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'M812', getLogFileName('out')])
        )
        print(command_to_start_test)
        osCommand(command_to_start_test)

        print()
    except Exception as e:
        print('error occur at the scheduler M812')

        # TODO: consider remove me
        from pprint import pprint
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


scheduler = BlockingScheduler()
scheduler.add_job(schedulerT1(), 'cron',
    minute='*/5')
# scheduler.add_job(schedulerM812, 'cron',
#     minute='5')
# scheduler.start()
# schedulerT1()
scheduler.start()
