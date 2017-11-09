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
    try:
        behave_command = 'behave -vk --no-capture  %s 2>&1 | tee %s' % (
            feature_file, result_pipe_to_file)
        return behave_command
        pass
    except Exception as e:
        print('error during generating behave command %s' % behave_command)
        raise e
    else:
        pass


def getAppiumProcessPid(android_serial):
    """get the target appium by the android_serial attached"""
    try:
        result = scheduler_lib.getPidOfProcess(['appium', android_serial])
        return result
        pass
    except Exception as e:
        print('error during getting result: %s' % result)
        raise e
    else:
        pass



def killAppiumProcess(appium_pids):
    output = []
    try:
        for appium_pid in appium_pids:
            output.append(subprocess.call('kill %s' % appium_pid, shell=True))
        pass
    except Exception as e:
        print('trying to kill appium process %s' % appium_pids)
    else:
        pass
    return output


def createAppiumCommand(android_serial, appium_port, appium_bootstrap_port):
    """to create the launchline for appium command

    Args:
        android_serial: the target android
        appium_port: the port appium listen on for commands
        appium_bootstrap_port: the port appium talk to the android

    Returns:
        Return1 : the pid of the appium
    """

    try:

        param = []
        param.append(APPIUM_BINARY)
        param.append(" ".join(["-U", android_serial]))
        param.append(" ".join(["-p", appium_port]))
        param.append(" ".join(['-bp', appium_bootstrap_port]))
        return ' '.join(param)
        pass
    except Exception as e:
        print('error during getting param: %s' % param)
        raise e
    else:
        pass



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
        time.sleep(5)

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


def kill_if_appium_process_exist(android_serial, max_retry):
    count_down = max_retry
    appium_pid = getAppiumProcessPid(android_serial)
    while count_down > 0 and appium_pid != [-1]:
        count_down -= 1
        print('try to kill old appium')
        killAppiumProcess(appium_pid)
        print('killing pid:%s' % appium_pid)
        time.sleep(10)
        appium_pid = getAppiumProcessPid(android_serial)


def schedulerT1():
    try:
        # STEP: kill old appium if possible
        print("STEP: kill old appium if possible")
        android_serial_T1 = 'VZHGLMA742804186'

        kill_if_appium_process_exist(android_serial_T1, 10)

        # STEP: start appium process
        print("STEP: start appium process")
        startAppiumProcess(
            android_serial_T1,
            '4723',
            '4724',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'T1', getAppiumLogFilename()])
        )

        time.sleep(10)

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
        # STEP: kill old appium if possible
        print("STEP: kill old appium if possible")
        android_serial_M812 = 'V2HGLMB721301100'

        appium_pid = getAppiumProcessPid(android_serial_M812)
        if appium_pid != -1:
            print('killing old appium')
            killAppiumProcess(appium_pid)
            time.sleep(10)

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
        print('dump the value of: appium_pid')
        pprint(appium_pid)
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

#schedulerM812()

scheduler = BlockingScheduler()
scheduler.add_job(schedulerT1, 'cron',
                  minute='*/20')
#scheduler.add_job(schedulerM812, 'cron',
#                  minute='*/5')
# scheduler.start()
# schedulerT1()
scheduler.start()
