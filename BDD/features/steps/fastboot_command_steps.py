#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# https://tinklabs.atlassian.net/wiki/spaces/ENG/pages/3871490/VZH+-+How+to+push+apk+into+devices

try:
    import sys
    import subprocess
    import re
    import platform
    from os import popen3 as pipe

    import subprocess, shlex
    from threading import Timer

    from pprint import pprint

except ImportError as e:
    print("[!] Required module missing. %s" % e.args[0])
    sys.exit(-1)

import re


# possible sequence to reset device
# check if device available
# fastboot devices

# fastboot oem fih on
# fastboot oem devlock key

# fastboot erase userdata
# fastboot erase cache
# fastboot erase oem


# to flash su rom
# fastboot devices

# fastboot oem fih on
# fastboot oem devlock key

# fastboot flash system /Users/louis_law/Downloads/boot-handySU-adb_0731.img.signed


# fastboot reboot


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





@step(u'FASTBOOT "{sCommand}"')
def step_impl(context, sCommand):
    sFastbootCommand = 'fastboot ' + sCommand

    (iReturnCode, sStdOut, sStdErr, bTimeout) = run(sFastbootCommand, timeout_sec=30)
    pprint((iReturnCode, sStdOut, sStdErr, bTimeout))
    assert iReturnCode == 0 and bTimeout == False

@step(u'FASTBOOT "{sCommand}", timeout {sTimeout} seconds')
def step_impl(context, sCommand, sTimeout):

    sFastbootCommand = 'fastboot ' + sCommand

    (iReturnCode, sStdOut, sStdErr, bTimeout) = run(sFastbootCommand, timeout_sec=int(sTimeout))
    pprint((iReturnCode, sStdOut, sStdErr, bTimeout))
    assert iReturnCode == 0 and bTimeout == False




@step(u'FASTBOOT Erase "{sPartitions}"')
def step_impl(context, sPartitions):
    """
        procedure to erase partition
    """

    # wait until bootloader ready
    context.execute_steps(u'''
        Given ADB Reboot bootloader
          And FASTBOOT unlock
    ''')
    for sPartition in sPartitions.split(','):
        # simple massage of input data
        sPartition=sPartition.strip()
        if sPartition in ['userdata', 'oem', 'cache','system']:
            context.execute_steps(u'''
                Then FASTBOOT "-i 0x489 erase %s"
            ''' % sPartition)

    context.execute_steps(u'''
        Then FASTBOOT "reboot"
    ''')
    pass

@step(u'FASTBOOT Erase userdata')
def step_impl(context):
    context.execute_steps(u'''
        Given ADB Reboot bootloader
          And FASTBOOT unlock
        Then FASTBOOT "-i 0x489 erase userdata"
        Then FASTBOOT "reboot"
    ''')
    pass



@step(u'FASTBOOT unlock')
def step_impl(context):
    context.execute_steps(u'''
        Then FASTBOOT "-i 0x489 oem fih on"
          And FASTBOOT "-i 0x489 oem devlock key"
    ''')

@step(u'FASTBOOT download image')
def step_impl(context):
    context.execute_steps(u'''
        Given ADB Reboot bootloader
        Then FASTBOOT "-i 0x489 oem fih on"
        Then FASTBOOT "-i 0x489 oem devlock key"
        Then FASTBOOT "-i 0x489 erase userdata"
        Then FASTBOOT "-i 0x489 erase oem"
        Then FASTBOOT "-i 0x489 flash system /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/handy-VZH-0-026A-00WW-system-1504271348.img", timeout 180 seconds
        Then FASTBOOT "-i 0x489 flash boot /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/boot-handy-adb-root-signed.img", timeout 60 seconds
        Then FASTBOOT "-i 0x489 flash recovery /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/handy-VZH-0-026A-00WW-recovery-0724.img", timeout 60 seconds
        Then FASTBOOT "-i 0x489 flash cda /home/logic/_workspace/handy_appium/_ref/VZH_image/6.0560/VZH-00WW-004-cda.img", timeout 60 seconds
            And FASTBOOT "reboot"
    ''')
    pass
