#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

import shlex

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='debug.log',
                    filemode='a')

from sys import platform


class processNotFoundException(Exception):
    pass


def normalize_string_to_list(object):
    output = object
    if type(output) == type([]):
        pass
    else:
        output = [str(object)]
    return output


def getPidOfProcess(texts_wanted):
    """to get the pid of the process by its grepable text

    Args:
        texts_wanted: the iconic text of the process

    Returns:
        Return1 : the pid of the process

    Assumption:
        single process per android_serial
    """

    texts_wanted = normalize_string_to_list(texts_wanted)

    try:
        pid_of_process = []
        commands = []
        commands.append('ps -ef')
        for text_wanted in texts_wanted:
            commands.append("grep -i '%s'" % text_wanted)
        commands.append("grep -v 'grep'")

        logging.debug('try to get the pid of the process')

        print('getting list of process')
        print_process_command = ' | '.join(commands)
        logging.debug(print_process_command)
        ps_list = os.popen(print_process_command).read().split('\n')

        from pprint import pprint
        print('dump the value of: ps_list')
        pprint(ps_list)

        for ps_printout in ps_list:

            # TODO: consider remove me

            if ps_printout.find(texts_wanted[0]) > -1:

                # from sys import platform
                if platform == "linux" or platform == "linux2":
                    # linux
                    print('the target process found')
                    pid_of_process.append(int(shlex.split(ps_printout)[1]))

                    logging.debug(pid_of_process)
                elif platform == "darwin":
                    # OS X
                    print('the target process found')
                    print(shlex.split(ps_printout))
                    pid_of_process.append(int(shlex.split(ps_printout)[1]))

                elif platform == "win32":
                    # Windows...
                    pass

        # NOTE: return -1 if not found
        if pid_of_process ==[]:
            pid_of_process == [-1]

        return pid_of_process

    except Exception as e:
        print('error during getting the pid of the process')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: process_wanted')
        pprint(texts_wanted)

        print('dump the value of: print_process_command')
        pprint(print_process_command)

        print('dump the value of: ps_list')
        pprint(ps_list)

        print('dump the value of: platform')
        pprint(platform)

        print('dump the value of: ps_printout')
        pprint(ps_printout)

        print('dump the value of: pid_of_process')
        pprint(pid_of_process)

        raise e
    else:
        pass


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
