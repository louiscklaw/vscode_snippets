import schedule
import time
import sys
import datetime

def osCommand(cmd):
    pyVesion = str(sys.version_info)
    if 'major=2' in pyVesion:
        import commands
        return commands.getoutput(cmd)
    else:
        import subprocess
        return subprocess.getoutput(cmd)


def jobA():
    # print("test")
    osCommand('python handyCall_Sender.py')

def jobB():
    # print("aaa")
    osCommand('python handyCall_Receiver.py')

def jobRecord():
    print(datetime.datetime.time(datetime.datetime.now()))


schedule.every(30).seconds.do(jobRecord)
schedule.every(5).minutes.do(jobA)
schedule.every(5).minutes.do(jobB)


# schedule.every(5).seconds.do(jobA)
# schedule.every(5).seconds.do(jobB)

while True:
    schedule.run_pending()
    time.sleep(1)