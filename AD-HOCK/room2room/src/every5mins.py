from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import datetime
import time
import logging

logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
           datafmt='%a, %d %b %Y %H:%M:%S',
            filename='/var/log/handyCallOut5Mins.txt',
            filemode='a')


def osCommand(cmd):
    pyVesion = str(sys.version_info)
    if 'major=2' in pyVesion:
        import commands
        return commands.getoutput(cmd)
    else:
        import subprocess
        return subprocess.getoutput(cmd)
def jobA():
    print(str(time.strftime("%Y%m%d-%H%M%S")) + " Start to execute R2R Call")
    osCommand('python handyCall_R2R_Sender.py')

def jobB():
    # print("aaa")
    osCommand('python handyCall_R2R_Receiver.py')

def dial_Sender():
    print(str(time.strftime("%Y%m%d-%H%M%S")) + " Start to execute Dail a Call")
    osCommand('python handyCall_Dial_Sender.py')

def dial_Receiver():
    # print("aaa")
    osCommand('python handyCall_Dial_Receiver.py')

def VE_Sender():
    print(str(time.strftime("%Y%m%d-%H%M%S")) + " Start to execute VE Call")
    osCommand("python handyCall_VE_Sender.py")

def VE_Receiver():
    osCommand("python handyCall_VE_Receiver.py")

def jobRecord():
    print(datetime.datetime.time(datetime.datetime.now()))

scheduler = BlockingScheduler()
scheduler.add_job(jobA, 'cron', minute='5,20,35,50')
scheduler.add_job(jobB, 'cron', minute='5,20,35,50')
scheduler.add_job(dial_Sender, 'cron', minute='10,25,40,55')
scheduler.add_job(dial_Receiver, 'cron', minute='10,25,40,55')
scheduler.add_job(VE_Sender, 'cron', minute='15,30,45,0')
scheduler.add_job(VE_Receiver, 'cron', minute='15,30,45,0')
scheduler.add_job(jobRecord, 'interval', seconds=30)
scheduler.start()
