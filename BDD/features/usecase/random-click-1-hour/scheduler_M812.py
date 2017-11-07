from apscheduler.schedulers.blocking import BlockingScheduler
import os, sys
import datetime
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datafmt='%a, %d %b %Y %H:%M:%S',
                    filename='%s' % __file__.replace('.py','.log'),
                    filemode='a')

PROJ_HOME = os.path.dirname(os.path.abspath(__file__))
RESULT_DIRECTORY = os.path.sep.join(
    [PROJ_HOME, './result'])

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
    print(getTodayString() + '.' + suffix)
    return getTodayString() + '.' + suffix


def osCommand(cmd):
    pyVesion = str(sys.version_info)
    if 'major=2' in pyVesion:
        import commands
        return commands.getoutput(cmd)
    else:
        import subprocess
        return subprocess.getoutput(cmd)


def behaveCommandConstructor(feature_file, result_pipe_to_file):
    return 'behave -vk --no-capture  %s | tee %s' % (feature_file, result_pipe_to_file)


def schedulerT1():
    try:
        command_to_start_test = behaveCommandConstructor(
            'random-click-1-hour_T1.feature',
            os.path.sep.join(
                [RESULT_DIRECTORY, 'T1', getLogFileName('out')])
        )
        print(command_to_start_test)
        osCommand(command_to_start_test)
    except Exception as e:
        print('error occur at the scheduler T1')

        # TODO: consider remove me
        from pprint import pprint
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

# scheduler.add_job(schedulerT1, 'cron',
#     minute='0')
scheduler.add_job(schedulerM812, 'cron',
    minute='5')

# scheduler.add_job(dial_Sender, 'cron', minute='10,25,40,55')
# scheduler.add_job(dial_Receiver, 'cron', minute='10,25,40,55')
# scheduler.add_job(VE_Sender, 'cron', minute='15,30,45,0')
# scheduler.add_job(VE_Receiver, 'cron', minute='15,30,45,0')
# scheduler.add_job(jobRecord, 'interval', seconds=30)
scheduler.start()
