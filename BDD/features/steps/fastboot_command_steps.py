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

class FASTBOOT():

    __adb_path = None
    __output = None
    __error = None
    __devices = None
    __target = None

    # reboot modes
    REBOOT_NORMAL = 0
    REBOOT_RECOVERY = 1
    REBOOT_BOOTLOADER = 2

    # default TCP/IP port
    DEFAULT_TCP_PORT = 5555
    # default TCP/IP host
    DEFAULT_TCP_HOST = "localhost"

    def __init__(self, adb_path="adb"):
        # By default we assume adb is in $PATH
        self.__adb_path = adb_path
        if not self.check_path():
            self.__error = "[!] adb path not valid"

    def __clean__(self):
        self.__output = None
        self.__error = None

    def __read_output__(self, fd):
        ret = ''
        while 1:
            line = fd.readline()
            if not line:
                break
            ret += line

        if len(ret) == 0:
            ret = None

        return ret

    def __build_command__(self, cmd):
        """
        Build command parameters
        """
        if self.__devices is not None and len(self.__devices) > 1 and self.__target is None:
            self.__error = "[!] Must set target device first"
            return None

        if type(cmd) is tuple:
            a = list(cmd)
        elif type(cmd) is list:
            a = cmd
        else:
            # All arguments must be single list items
            a = cmd.split(" ")

        a.insert(0, self.__adb_path)
        if self.__target is not None:
            # add target device arguments to the command
            a.insert(1, '-s')
            a.insert(2, self.__target)

        return a

    def run_cmd(self, cmd):
        """
        Run a command against the adb tool ($ adb <cmd>)
        """
        self.__clean__()

        if self.__adb_path is None:
            self.__error = "[!] ADB path not set"
            return False

        try:
            args = self.__build_command__(cmd)
            if args is None:
                return
            cmdp = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.__output, self.__error = cmdp.communicate()
            retcode = cmdp.wait()
            if "device unauthorized" in self.__output:
                self.__error = "[-] Device unauthorized"
                return False
            return self.__output.rstrip('\n')
        except OSError, e:
            self.__error = str(e)

        return


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


@step(u'FASTBOOT Erase userdata,oem')
def step_impl(context):
    context.execute_steps(u'''
        Given ADB Reboot bootloader
        Then FASTBOOT "-i 0x489 oem fih on"
        Then FASTBOOT "-i 0x489 oem devlock key"
        Then FASTBOOT "-i 0x489 erase userdata"
        Then FASTBOOT "-i 0x489 erase oem"
        Then FASTBOOT "reboot"
    ''')
    pass

@step(u'FASTBOOT Erase userdata')
def step_impl(context):
    context.execute_steps(u'''
        Given ADB Reboot bootloader
        Then FASTBOOT "-i 0x489 oem fih on"
        Then FASTBOOT "-i 0x489 oem devlock key"
        Then FASTBOOT "-i 0x489 erase userdata"
        Then FASTBOOT "reboot"
    ''')
    pass





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
