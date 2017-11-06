#!/usr/bin/env python
# coding:utf-8

try:
    import sys
    import subprocess
    import re
    import platform
    from os import popen3 as pipe

    import subprocess
    import shlex
    from threading import Timer
    from time import sleep

    from pprint import pprint

    import logging

except ImportError as e:
    print("[!] Required module missing. %s" % e.args[0])
    sys.exit(-1)

import re


def get_index_by_serial(index_serial_pair, serial):
    """
        try to get index by serial number
        Args:
            - index_serial_pair - output from adb.get_devices() / fastboot.get_devices()
    """

    return {
        serial: idx
        for (idx, serial) in index_serial_pair.items()
    }[serial]


def kill_proc(proc, timeout):
    timeout["value"] = True
    proc.kill()


def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(
        cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = {"value": False}
    timer = Timer(timeout_sec, kill_proc, [proc, timeout])
    timer.start()
    stdout, stderr = proc.communicate()
    timer.cancel()
    return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), timeout["value"]


@step(u'Fastboot init')
def step_impl(context):
    """
    To initialize fastboot session
    implict reboot by adb occur.
    """
    try:
        if hasattr(context, 'android_serial'):
            sleep(3)
            print('android_serial:%s is used for fastboot')

            print('reboot device by adb')
            context.execute_steps(u'''
                Then ADB Reboot bootloader
            ''')

            # NOTE: this is a small technique for using the fastboot library.
            # the get_devices also update the list inside the library.
            f_session = context.fastboot_session

            f_session.set_target_by_id(
                get_index_by_serial(f_session.get_devices(),
                                    context.android_serial)
            )
        else:
            # NOTE: no android_serial info here. assert error
            print('android_serial not found')
            assert False, 'android_serial not found'

    except Exception as e:
        print('error during Fastboot init')
        raise e
    else:
        pass


@step(u'FASTBOOT "{sCommand}"')
def step_impl(context, sCommand):
    try:
        sFastbootCommand = 'fastboot ' + sCommand

        (iReturnCode, sStdOut, sStdErr, bTimeout) = run(
            sFastbootCommand, timeout_sec=30)
        pprint((iReturnCode, sStdOut, sStdErr, bTimeout))
        assert iReturnCode == 0 and bTimeout == False

        pass
    except Exception as e:
        print('error during FASTBOOT %s' % sCommand)
        raise e
    else:
        pass



@step(u'FASTBOOT "{sCommand}", timeout {sTimeout} seconds')
def step_impl(context, sCommand, sTimeout):

    sFastbootCommand = 'fastboot ' + sCommand

    (iReturnCode, sStdOut, sStdErr, bTimeout) = run(
        sFastbootCommand, timeout_sec=int(sTimeout))
    pprint((iReturnCode, sStdOut, sStdErr, bTimeout))
    assert iReturnCode == 0 and bTimeout == False


@step(u'FASTBOOT Erase "{sPartitions}"')
def step_impl(context, sPartitions):
    """procedure to erase partition"""

    try:

        # wait until bootloader ready
        context.execute_steps(u'''
            Given ADB Reboot bootloader
            And FASTBOOT unlock
        ''')
        for sPartition in sPartitions.split(','):
            # simple massage of input data
            sPartition = sPartition.strip()
            if sPartition in ['userdata', 'oem', 'cache', 'system']:
                context.execute_steps(u'''
                    Then FASTBOOT "-i 0x489 erase %s"
                ''' % sPartition)

        context.execute_steps(u'''
            Then FASTBOOT "reboot"
        ''')
        print('erase partition done')

    except Exception as e:
        print('error during erase paritions %s' % sPartition)
        raise e
    else:
        pass


@step(u'FASTBOOT Erase userdata')
def step_impl(context):
    """
    stored procedure to erase user data by fastboot
    """

    try:
        if hasattr(context, 'device'):
            print('perform fastboot erase userdata')
            if context.device == 'M812':
                context.execute_steps(u'''
                    Then FASTBOOT "erase userdata"
                    And FASTBOOT "reboot"
                ''')
                pass
            elif context.device == 'T1':
                context.execute_steps(u'''
                    Then FASTBOOT unlock
                    And FASTBOOT "-i 0x489 erase userdata"
                    And FASTBOOT "reboot"
                ''')
            else:
                print('unhandled fastboot rease userdata')
                assert False
                pass
        else:
            # Temporary default action for T1
            # TODO: put it into if branch, as currently the context.device didn't implement there yet. so i need put it here
            context.execute_steps(u'''
                Given ADB Reboot bootloader
                    And FASTBOOT unlock
                    Then FASTBOOT "-i 0x489 erase userdata"
                    Then FASTBOOT "reboot"
            ''')
            pass
        pass
    except Exception as e:
        print('error during Fastboot Erase userdata')
        raise e
    else:
        pass

@step(u'FASTBOOT unlock')
def step_impl(context):
    if hasattr(context, 'device'):
        if context.device == 'M812':
            pass
        elif context.device == 'T1':
            context.execute_steps(u'''
                Then FASTBOOT "-i 0x489 oem fih on"
                And FASTBOOT "-i 0x489 oem devlock key"
            ''')
        else:
            print('unhandled fastboot unlock')
            assert False
            pass
    else:
        # Temporary default action for T1
        # TODO: put it into if branch, as currently the context.device didn't implement there yet. so i need put it here
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


@step(u'fastboot erase M812')
def step_impl(context):
    context.execute_steps(u'''
        Given ADB Reboot bootloader
            Then FASTBOOT " erase userdata"
            Then FASTBOOT "reboot"
    ''')
