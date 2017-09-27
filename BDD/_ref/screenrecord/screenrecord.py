#!/usr/bin/python

# command line:
#  ./screenrecord.py 180 ~/_temp/
try:
    import sys
    import subprocess
    import re
    import platform
    from os import popen3 as pipe
    from time import sleep
    from datetime import datetime
    import subprocess, shlex
    from threading import Timer

    from pprint import pprint

except ImportError as e:
    print("[!] Required module missing. %s" % e.args[0])
    sys.exit(-1)

import re


iVideoRecordRetryTime = 15

def kill_proc(proc, timeout):
    timeout["value"] = True
    proc.kill()

def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = {"value": False}
    timer = Timer(timeout_sec, kill_proc, [proc, timeout])
    timer.start()
    stdout, stderr = proc.communicate()
    timer.cancel()
    return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), timeout["value"]


def VideoRecord(sFileName, iDuration):
    iDuration = min([iDuration, 180])
    # echo "adb pull /sdcard/$sc.mp4  &&  adb shell rm /sdcard/$sc.mp4"

    try:
        print('wait adb ready')
        (iReturnCode, sStdOut, sStdErr, bTimeout)=run('adb wait-for-device', timeout_sec=300)
        if iReturnCode != 0:
            raise('Err while adb ready')

        print('wait until /sdcard ready')
        (iReturnCode, sStdOut, sStdErr, bTimeout)=run("adb shell 'ls -l /sdcard'", timeout_sec=300)
        print('screenrecord:lsL:output:%d:%s:%s' % (iReturnCode,sStdOut, sStdErr ) )
        if iReturnCode != 0 :
            raise('Error while fetching /sdcard directory')
        elif sStdErr.find('Unable to open') > -1:
            raise('Error while fetching /sdcard directory')
        else:
            print('recording... timelimit=%d' % iDuration)
            (iReturnCode, sStdOut, sStdErr, bTimeout)=run('adb shell screenrecord --bit-rate 3000000 /sdcard/%s.mp4   --time-limit %s ' % (sFileName, iDuration), timeout_sec=iDuration+3)
            if iReturnCode ==0:
                pass
            else:
                print('screenrecord:iReturnCode:%s' % iReturnCode)
                print('screenrecord:sStdErr:%s' % sStdErr)
                raise('Error while fetching /sdcard directory')
        pass

    except Exception as e:
        print('wait %s seconds retry...' % iVideoRecordRetryTime)
        sleep(iVideoRecordRetryTime)

    except KeyboardInterrupt as e:
        print('ctrl-c end')
        sys.exit()
        pass

    pass


def SendFileToPC(sPathOnAndroid, sPathOnPC):
    #adb pull /sdcard/$sc.mp4  &&  adb shell rm /sdcard/$sc.mp4
    dParameters={}
    dParameters['sPathOnAndroid']=sPathOnAndroid
    dParameters['sPathOnPC']=sPathOnPC


    print('copying file...')

    (iRetrunCode, sStdOut, sStdErr, bTimeout) = run('adb shell "ls -1 /sdcard/*.mp4"', timeout_sec=3)
    for sFile in sStdOut.split('\n'):
        dParameters['sFile'] = sFile
        
        print('file on android %s' % sFile)
        (iReturnCode, sStdOut, sStdErr, bTimeout)=run('adb pull %(sFile)s  %(sPathOnPC)s' % dParameters, timeout_sec=10)
        if iReturnCode == 0:
            run('adb shell rm %(sFile)s' % dParameters, timeout_sec=10)

    pass


i=0

try:
    while 1:
        i+=1
        iDuration = int(sys.argv[1])
        sVideoFileName = datetime.now().strftime('%s')
        
        print('recording count %d' % i)
        
        VideoRecord(sVideoFileName, iDuration)
        SendFileToPC(sVideoFileName, sys.argv[2])
        pass
except KeyboardInterrupt as e:
    print('ctrl-c end')
    sys.exit()
    pass