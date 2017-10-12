#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

from behave import given, when, then, step
from common import *

import traceback

from time import sleep
from datetime import datetime

from pyand import ADB, Fastboot

from pprint import pprint

import subprocess
import shlex
from threading import Timer

sys.path.append(os.path.dirname(__file__) + '/../_lib')
from android_const import android_key_const

import pexpect


PATH_PC_LIB = os.path.dirname(__file__) + '/../_lib/shell_script'
PATH_ANDROID_TEMP = r'/data/local/tmp'

FILE_TINKLABS1001 = r'tinklabs1001'
FILE_CHANGE_SETTINGS = r'change_settings.sh'
FILE_CHANGE_PROP = r'change_prop.sh'

FILE_CHANGE_WPA_SUPPLICANT = r'change_wifi.sh'
FILE_WPA_SUPPLICANT = r'wpa_supplicant.conf'

PATH_PC_TINKLABS1001 = '/'.join([PATH_PC_LIB, FILE_TINKLABS1001])
PATH_PC_CHANGE_SETTINGS = '/'.join([PATH_PC_LIB, FILE_CHANGE_SETTINGS])
PATH_PC_CHANGE_PROP = '/'.join([PATH_PC_LIB, FILE_CHANGE_PROP])

PATH_ANDROID_TINKLABS1001 = '/'.join([PATH_ANDROID_TEMP, FILE_TINKLABS1001])
PATH_ANDROID_CHANGE_SETTINGS = '/'.join(
    [PATH_ANDROID_TEMP, FILE_CHANGE_SETTINGS])
PATH_ANDROID_CHANGE_PROP = '/'.join([PATH_ANDROID_TEMP, FILE_CHANGE_PROP])

PATH_PC_WPA_SUPPLICANT_CONF = '/'.join([PATH_PC_LIB, FILE_WPA_SUPPLICANT])
PATH_PC_CHANGE_WPA_SUPPLICANT = '/'.join(
    [PATH_PC_LIB, FILE_CHANGE_WPA_SUPPLICANT])
PATH_ANDROID_CHANGE_WPA_SUPPLICANT = '/'.join(
    [PATH_ANDROID_TEMP, FILE_CHANGE_WPA_SUPPLICANT])

PATH_ANDROID_WIFI_WPA_SUPPLICANT = r'/data/misc/wifi/wpa_supplicant.conf'
PATH_ANDROID_WIFI_WPA_SUPPLICANT_BACKUP = r'/data/local/tmp/wpa_supplicant.bak'


dParameters = {}
dParameters['PATH_PC_LIB'] = PATH_PC_LIB
dParameters['PATH_PC_TINKLABS1001'] = PATH_PC_TINKLABS1001
dParameters['PATH_PC_CHANGE_SETTINGS'] = PATH_PC_CHANGE_SETTINGS
dParameters['PATH_PC_CHANGE_PROP'] = PATH_PC_CHANGE_PROP

dParameters['PATH_PC_WPA_SUPPLICANT_CONF'] = PATH_PC_WPA_SUPPLICANT_CONF
dParameters['PATH_PC_CHANGE_WPA_SUPPLICANT'] = PATH_PC_CHANGE_WPA_SUPPLICANT

dParameters['PATH_ANDROID_TEMP'] = PATH_ANDROID_TEMP
dParameters['PATH_ANDROID_TINKLABS1001'] = PATH_ANDROID_TINKLABS1001
dParameters['PATH_ANDROID_CHANGE_SETTINGS'] = PATH_ANDROID_CHANGE_SETTINGS
dParameters['PATH_ANDROID_CHANGE_PROP'] = PATH_ANDROID_CHANGE_PROP

dParameters['PATH_ANDROID_CHANGE_WPA_SUPPLICANT'] = PATH_ANDROID_CHANGE_WPA_SUPPLICANT


# tinklabs-X555LNB% sudo fastboot -i 0x489 devices
# VZHGLMA750300169        fastboot

# fastboot oem fih on
# fastboot oem devlock key

# fastboot erase userdata
# fastboot erase oem

class adb_command():
    def __init__():
        pass

    def run_command(command):
        self.run


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


def get_epoch_time():
    """
        return the epoch of current time
    """
    return int(datetime.now().strftime('%s'))


def get_time_difference_to(given_time):
    """
    calculate the different (in seconds) between now and the given time

    Args:
        given_time: the int(in epoch format) want to check

    Returns:
        the time different between now and the given_time

    """
    return get_epoch_time() - given_time


@step(u'ADB Wait for device')
def step_impl(context):
    if hasattr(context, 'adb_session'):
        pass
    else:
        # context.adb_session = ADB()
        logging.debug('adb_session is missing')
        assert False, 'adb_session is missing'

    adb = context.adb_session
    adb.run_cmd('wait-for-device')
    sleep(3)


@step(u'ADB Wait for device, timeout {sSeconds} seconds')
def step_impl(context, sSeconds):
    """
        probe the device by adb wait-for-device command.
    """
    time_to_start = get_epoch_time()

    context.adb_session.run_cmd('wait-for-device')

    # (iRetrunCode, sStdOut, sStdErr, bTimeout) = result
    context.time_poweron_to_adb_ready = get_time_difference_to(time_to_start)

    # wait some seconds more to let device ready
    sleep(3)

    pass

# TODO: delete
# @step(u'ADB Reboot bootloader "{android_serial}"')
# def step_impl(context, android_serial):
#     """
#         to be replaced by
#     """
#     (iRetrunCode, sStdOut, sStdErr, bTimeout) = run(
#         'adb -s %s reboot bootloader' % android_serial,
#         timeout_sec=int(sSeconds))


@step(u'ADB Reboot bootloader')
def step_impl(context):
    """
        reboot the android by adb command adb reboot
    """
    if hasattr(context, 'adb_session'):
        pass
    else:
        assert False, "adb_session not found"

    adb = context.adb_session
    adb.run_cmd('reboot bootloader')
    sleep(5)


@step(u'ADB Reboot device')
def step_impl(context):
    """
        to be obsoleted, reboot device
    """
    if hasattr(context, 'adb_session'):
        pass
    else:
        # TODO: remove me
        context.adb_session = ADB()

    adb = context.adb_session
    adb.run_cmd('reboot')
    sleep(5)


@step(u'ADB PATH_ANDROID_TEMP directory is ready, timeout {sSeconds} seconds')
def step_impl(context, sSeconds):
    """
    check if the filesystem in android is ready

    Args:
        sSeconds: seconds until timeout
    """
    time_to_end = int(get_epoch_time()) + int(sSeconds)
    bDirectoryReady = False

    while time_to_end > int(get_epoch_time()):
        # (iReturnCode, sStdOut, sStdErr, bTimeout)=run('adb shell ls -l %s' % PATH_ANDROID_TEMP, timeout_sec=5)

        result = context.adb_session.run_cmd(
            'shell ls -l %s' % PATH_ANDROID_TEMP)

        # if iReturnCode == 0 :
        if result.find('No such file or directory') > -1:
            pass
        else:
            bDirectoryReady = True
            break

    if bDirectoryReady:
        pass
    else:
        logging.error('cannot get android temp direcotory')
        assert False
    pass


@step(u'ADB Initialize android')
def step_impl(context):
    """
    packed action to initialize android
    """
    context.execute_steps(u'''
        Given ADB PATH_ANDROID_TEMP directory is ready, timeout 60 seconds
            And ADB push tinklabs1001
            And ADB push change_settings

        Then ADB change permission tinklabs1001
            And ADB change permission change_prop

        Then ADB settings put global package_verifier_enable 0
            And ADB settings put global stay_on_while_plugged_in 7

        Then ADB settings put secure install_non_market_apps 1
            And ADB settings put secure screen_off_timeout 600000000
            And ADB settings put secure screensaver_activate_on_sleep 0
            And ADB settings put secure screensaver_components com.google.android.deskclock/com.android.deskclock.Screensaver
            And ADB settings put secure screensaver_default_component com.google.android.deskclock/com.android.deskclock.Screensaver
            And ADB settings put secure screensaver_enabled 0

        Then ADB settings put system dim_screen 0
            And ADB settings put system screen_brightness 10
            And ADB settings put system screen_off_timeout 600000000
            And ADB settings put system transition_animation_scale 0
            And ADB settings put system window_animation_scale 0

            # disable USB file transfer
            # And ADB setprop "persist.sys.usb.config" "adb,mtp"
      ''')


# TODO: delete me
@step(u'ADB Init session')
def step_impl(context):
    context.adb_session = ADB()


@step(u'ADB adb push "{sSourceFile}" "{sTargetFile}"')
def step_impl(context, sSourceFile, sTargetFile):
    """
        to handle file coping from PC to android
        TODO: obsolete

        "Args":
            - sSourceFile - Source file from PC
            - sTargetFile - Target file in android
    """
    # adb = context.adb_session
    # adb.push_local_file(sSourceFile, sTargetFile)

    # adb.run_cmd('push %s %s' %(sSourceFile, sTargetFile))
    # subprocess.check_output(
    #     'adb push %s %s' % (sSourceFile, sTargetFile)
    #     ,shell= True)

    context.adb_session.run_cmd(
        'push %s %s' % (sSourceFile, sTargetFile)
    )

    pass


@step(u'ADB push "{sSourceFile}" "{sTargetFile}"')
def step_impl(context, sSourceFile, sTargetFile):
    """
        to handle file coping from PC to android

        "Args":
            - sSourceFile - Source file from PC
            - sTargetFile - Target file in android
    """
    print('i am supposed to adb push %s %s' % (sSourceFile, sTargetFile))
    run('adb push %s %s' % (sSourceFile, sTargetFile), timeout_sec=10)
    pass


@step(u'ADB change permission "{sPermission}" "{sTargetFile}"')
def step_impl(context, sTargetFile, sPermission):
    """
        to change the permission of file
    """
    context.execute_steps(u'''
        Then ADB shell "chmod %s %s"
    ''' % (sPermission, sTargetFile))
    pass


@step(u'ADB push tinklabs1001')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB push "%(PATH_PC_TINKLABS1001)s" "%(PATH_ANDROID_TEMP)s"
    ''' % dParameters)


@step(u'ADB change permission tinklabs1001')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB change permission "777" "%(PATH_ANDROID_TINKLABS1001)s"
    ''' % dParameters)


@step(u'ADB change permission change_settings')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB change permission "777" "%(PATH_ANDROID_CHANGE_SETTINGS)s"
    ''' % dParameters)
    pass


@step(u'ADB change permission change_prop')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB change permission "777" "%(PATH_ANDROID_CHANGE_PROP)s"
    ''' % dParameters)
    pass


@then(u'ADB change permission change_wpa_supplicant')
def step_impl(context):
    # NOTE: to be obsoleted
    logging.debug('Then ADB change permission change_wpa_supplicant')
    context.execute_steps(u'''
        Then ADB change permission "777" "%(PATH_ANDROID_CHANGE_WPA_SUPPLICANT)s"
    ''' % dParameters)


@step(u'ADB push change_settings')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB push "%(PATH_PC_CHANGE_SETTINGS)s" "%(PATH_ANDROID_TEMP)s"
    ''' % dParameters)


@step(u'ADB push change_prop')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB push "%(PATH_PC_CHANGE_PROP)s" "%(PATH_ANDROID_TEMP)s"
    ''' % dParameters)


@step(u'ADB push change_wpa_supplicant')
def step_impl(context):
    context.execute_steps(u'''
        Then ADB push "%(PATH_PC_CHANGE_WPA_SUPPLICANT)s" "%(PATH_ANDROID_TEMP)s"
    ''' % dParameters)


# VZH:/ $ settings
# usage:  settings [--user <USER_ID> | current] get namespace key
#         settings [--user <USER_ID> | current] put namespace key value
#         settings [--user <USER_ID> | current] delete namespace key
#         settings [--user <USER_ID> | current] list namespace
@step(u'ADB settings put {sNamespace} {sSettingName} {sValue}')
def step_impl(context, sValue, sSettingName, sNamespace):
    """
        to handle the google application verification before test run
        :Args:
            - sValue - value of package_verifier_enable wanted
    """
    logging.debug('I am supposed to change the %s to %s' %
                  (sSettingName, sValue))

    # TODO: better implementation

    # context.execute_steps(u'''
    #     Then ADB shell ""source /data/local/tmp/change_settings.sh put %s %s %s""
    # ''' % (sNamespace, sSettingName, sValue))

    context.execute_steps(u'''
        Then adb root shell "settings put %s %s %s"
    ''' % (sNamespace, sSettingName, sValue))

    pass


@step(u'ADB settings get {sNamespace} {sKey}')
def step_adb_settings_get(context, sNamespace, sKey):
    """
        a wrapper for adb settings get <namespace> <key>
    """

    return run('adb shell settings get %s %s' % (sNamespace, sKey), timeout_sec=5)


@step(u'ADB settings {sNamespace} {sKey} should be {sExpected}')
def step_adb_settings_compare(context, sNamespace, sKey, sExpected):
    """
        getting value from adb settings, with checking
    """
    # (sReturnCode, sStdOut, sStdErr, sTimeout) = step_adb_settings_get(context, sNamespace, sKey)
    # assert sExpected == sStdOut.strip()
    return context.adb_session.run_cmd(
        'shell settings get %s %s' % (sNamespace, sKey)
    )


# setprop, getprop
# usage: setprop NAME VALUE

# Sets an Android system property.

@step(u'ADB setprop "{sName}" "{sValue}"')
def step_impl(context, sName, sValue):
    """
        to handle the google application verification before test run
        :Args:
            - sValue - value of package_verifier_enable wanted
    """
    print(u'STEP: Given ADB setprop "%s" "%s"' % (sName, sValue))

    # context.execute_steps(u'''
    #     Given ADB Init session
    #         And ADB push tinklabs1001
    #         And ADB push change_prop

    #     Then ADB change permission tinklabs1001
    #         And ADB change permission change_prop

    #     Then ADB shell ""%s -c 'setprop %s %s'""
    #     Then ADB shell ""source /data/local/tmp/change_prop.sh setprop %s %s %s""
    # ''' % (dParameters['PATH_ANDROID_TINKLABS1001'], sName, sValue))

    context.execute_steps(u'''
        Given ADB Init session
            And ADB push tinklabs1001
            And ADB push change_prop

        Then ADB change permission tinklabs1001
            And ADB change permission change_prop

        Then ADB shell "source %s setprop %s %s"
    ''' % (dParameters['PATH_ANDROID_CHANGE_PROP'], sName, sValue))

    print('change props %s done' % sName)

    pass


@step(u'ADB getprop "{sName}"')
def step_adb_getprop(context, sName):
    """
        to handle adb shell getprop
    """
    # return run('adb shell getprop %s' % (sName), timeout_sec=5)
    return context.adb_session.run_cmd('shell getprop %s' % (sName))


@step(u'ADB prop "{sName}" should be "{sExpected}"')
def step_impl(context, sName, sExpected):
    """
        to compare the prop with the expected value
    """
    print(u'STEP: Given ADB getprop "{sName}" should be "{sExpected}"')
    # (sReturnCode, sStdOut, sStdErr, sTimeout) = step_adb_getprop(context, sName)
    sStdOut = step_adb_getprop(context, sName)
    print('props returned: %s' % sStdOut.strip())
    assert sExpected == sStdOut.strip()


@step(u'ADB setprop test with shell True')
def step_impl(context):
    logging.debug('STEP: Given ADB setprop test with shell True')
    context.execute_steps(u'''
        Given ADB Init session
            And ADB push tinklabs1001
            And ADB push change_prop

        Then ADB change permission tinklabs1001
            And ADB change permission change_prop
    ''')


@step(u'ADB disable usb mass storage')
def step_disable_usb_mass_storage(context):
    """
        disable usb mass storage function on the device
    """
    logging.debug('STEP: disable usb mass storage')
    context.execute_steps(u'''
        Given ADB Init session
            And ADB push tinklabs1001
            And ADB push change_prop

        Then ADB change permission tinklabs1001
            And ADB change permission change_prop
    ''')
    pass


@step(u'ADB screen capture, save to "{sTargetPath}"')
def step_impl(context, sTargetPath):
    """
        simple facility to provide screen capture
        TODO: generalize me
    """
    try:
        # adb shell screencap -p /sdcard/$sc.png
        # try:
        dParameter = {}
        dParameter['sEpoch'] = datetime.now().strftime('%s')
        dParameter['sTargetPath'] = sTargetPath
        dParameter['sTargetPathWithDatetime'] = os.path.join(
            dParameter['sTargetPath'], dParameter['sEpoch'])

        lsADBCommand = []
        lsADBCommand.append(
            'shell screencap -p /sdcard/%(sEpoch)s.png' % dParameter)
        lsADBCommand.append(
            'pull /sdcard/%(sEpoch)s.png %(sTargetPathWithDatetime)s' % dParameter)
        lsADBCommand.append('shell rm /sdcard/%(sEpoch)s.png' % dParameter)
        lsADBCommand.append('shell uiautomator dump')
        lsADBCommand.append(
            'pull /sdcard/window_dump.xml %(sTargetPathWithDatetime)s/dump.uix' % dParameter)
        lsADBCommand.append('shell rm /sdcard/window_dump.xml' % dParameter)

        # NOTE create a landing directory for screen capture
        os.makedirs(dParameter['sTargetPathWithDatetime'], 0755)

        adb = context.adb_session
        for sADBCommand in lsADBCommand:
            adb.run_cmd(sADBCommand)
    except Exception:
        traceback.print_stack()
        print('--------------')
        traceback.print_exc()

    pass


@step(u'ADB video capture, save it to "{sTargetFile}"')
def step_impl(context, sTargetFile):
    """
        start the video capture on the phone, store it to the phone's path given by sTargetFile

        :Args:
            - sTargetFile - target file path to store the video capture
            return a pid of the adb shell screenrecord
    """
    print(u'I am supposed start video capture')
    sCommand = 'adb shell screenrecord --bit-rate 3000000 %s' % sTargetFile
    proc = subprocess.Popen(shlex.split(sCommand),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    context.adbScreenRecord = proc
    pass


@step(u'ADB stop video capture process')
def step_impl(context):
    """
        kill the process of adb shell screenrecord if possible,
    """
    print(u'I am supposed to kill the adb screenrecord process')
    try:
        run('kill %d' % context.adbScreenRecord.pid, timeout_sec=10)
        pass
    except Exception as e:
        pass
    pass


@step(u'ADB pull "{sSourceFile}" "{sTargetFile}"')
def step_impl(context, sSourceFile, sTargetFile):
    """
        to upload a file from phone to PC

        :Args:
            - sSourceFile - the source file from the device
            - sTargetFile - the target path to save the video
    """
    print('I am supposed upload video capture, save to "%s"' % sTargetFile)
    run('adb pull %s %s' % (sSourceFile, sTargetFile), timeout_sec=60)


@step(u'ADB shell "{command}"')
def step_adb_shell(context, command):
    """
        send command using adb shell

        :Args:
            - command - command would like to pass to adb shell
    """
    adb_command = 'shell %s' % command
    # print('i am supposed to run adb command %s' % sAdbCommand)
    # (iResultCode, sStdOut, sStdErr, bTimeout) = run(sAdbCommand, timeout_sec = 5)

    context.adb_command_result = context.adb_session.run_cmd(adb_command)
    pass


@step(u'ADB command result should be "{text}"')
def step_impl(context, text):
    if text == context.adb_command_result.strip():
        pass
    else:
        print_fail('text:%s' % text)
        print_fail('context.adb_command_result:%s' %
                   context.adb_command_result)
        assert False


@step(u'ADB setup wifi')
def step_impl(context):
    """
        try to setup wifi before phone boots up
        TODO: remove the hardcode on last part
    """

    context.execute_steps(u'''
        Then ADB push tinklabs1001
            And ADB change permission tinklabs1001

        Then ADB push change_wpa_supplicant
            And ADB change permission change_wpa_supplicant

        Then ADB push wpa_supplicant
        Then ADB shell ""/data/local/tmp/change_wifi.sh""
    ''')
    # pprint(run('''adb shell "/data/local/tmp/change_wifi.sh"''',
    # timeout_sec=5
    # ))
    assert False


@then(u'ADB push wpa_supplicant')
def step_impl(context):
    print(u'STEP: Then ADB push wpa_supplicant')

    context.execute_steps(u'''
        Then ADB push "%(PATH_PC_WPA_SUPPLICANT_CONF)s" "%(PATH_ANDROID_TEMP)s"
    ''' % dParameters)


@step(u'ADB check boot completed, timeout {sSeconds} seconds')
def step_impl(context, sSeconds):
    """
        to track the device status at fixed 15 seconds interval
        :Args:
            - sSeconds - timeout for the process
    """
    bBootComplete = False
    sStdOut = ''
    sStdErr = ''

    time_start = get_epoch_time()
    time_to_end = time_start + int(sSeconds)

    # for i in range(0, int(sSeconds)):
    while time_to_end > get_epoch_time():
        sleep(15)
        # (sResultCode, sStdOut, sStdErr, bTimeout) = step_adb_getprop(context, "sys.boot_completed")
        sStdOut = step_adb_getprop(context, 'sys.boot_completed')
        sStdOut = sStdOut.strip()

        if sStdOut == '1':
            bBootComplete = True
            break

    if bBootComplete:
        context.time_sys_boot_animation = get_time_difference_to(time_start)
        pass
    else:
        logging.error('boot failed')
        logging.error('sStdOut: %s' % sStdOut)
        assert False


@then(u'Fail if the time taken "{name_of_process}" is more than {seconds} seconds')
def step_impl(context, name_of_process, seconds):
    """
        to fail the test if the time take by name_of_process is larger than a give time
    """
    print(u'STEP: Fail if the time taken %s is more than %s seconds' %
          (name_of_process, seconds))

    challenger_time = eval('context.%s' % name_of_process)

    try:
        if int(challenger_time) > int(seconds):
            print_fail('challenger %s time %d' %
                       (name_of_process, int(challenger_time)))
            assert False
        else:
            print_verdict('challenger %s time %d is less than %d' % (
                name_of_process, int(challenger_time), int(seconds)))

    except Exception:
        # TODO: a error class here
        print('exception raise during measure the time')
        traceback.print_stack()
        print('--------------')
        traceback.print_exc()
        assert False
        pass


def send_command_to_adb(adb_shell_process, command_to_send, texts_expected):
    """
        send command to adb shell and wait for ready
    """

    logging.error(command_to_send)
    adb_shell_process.sendline(command_to_send)
    texts_expected.append(pexpect.TIMEOUT)
    return adb_shell_process.expect(texts_expected)


@step(u'adb root shell "{command}"')
def step_adb_root_shell(context, command):
    """
        send command by root shell (tinklabs1001)
        this is a workaround as tinklabs1001 -c {command} doesn't work

        :Args:
            - command - command would like to send by root shell
    """
    logging.basicConfig(level=logging.DEBUG)

    adb_commands = []
    adb_commands.append((PATH_ANDROID_TINKLABS1001, ['#']))
    adb_commands.append((command, ['#']))

    child = pexpect.spawn(
        context.adb_binary + " -s %s shell" % context.android_serial
    )
    index = child.expect(["$", "@", pexpect.TIMEOUT])

    for (command_to_send, text_expected) in adb_commands:
        logging.error('sending %s' % command_to_send)
        send_command_to_adb(
            child, command_to_send, text_expected)


@then(u'inject wifi configuration "{wifi_configuration}" to android')
def step_impl(context, wifi_configuration):
    logging.debug(u'STEP: Then inject wifi configuration to android')

    context.execute_steps(u'''
        Then ADB backup wifi configuration
          And adb root shell "cat %s >> %s"
    ''' % (wifi_configuration, PATH_ANDROID_WIFI_WPA_SUPPLICANT))


@step(u'ADB svc {subcommand} {control}')
def step_impl(context, subcommand, control):
    """
    Available commands:
    help     Show information about the subcommands
    power    Control the power manager
    data     Control mobile data connectivity
    wifi     Control the Wi-Fi manager
    usb      Control Usb state
    """
    context.execute_steps(u'''
        Then adb root shell "svc %s %s"
    ''' % (subcommand, control))


@then(u'ADB restart wifi')
def step_impl(context):
    logging.debug(u'STEP: Then adb restart wifi')

    context.execute_steps(u'''
        Then adb root shell "svc wifi disable"
    ''')
    sleep(5)


@then(u'Fail if the android cannot ping to {host}')
def step_impl(context, host):
    logging.debug(u'STEP: Then Fail if the android cannot ping to %s' % host)

    result = context.adb_session.run_cmd('''shell ping -c 5 %s ''' % host)

    if result.find('unknown host') > -1:
        logging.error(result)
        assert False, "cannot connect to internet"


@then(u'ADB check if file exist {file}')
def step_impl(context, file):
    """
        IDEA/TODO: do i need this ?
    """


@then(u'ADB backup wifi configuration')
def step_impl(context):
    logging.debug(u'STEP: Then ADB backup wifi configuration')

    context.execute_steps(u'''
        Then adb root shell "cp %s %s"
    ''' % (PATH_ANDROID_WIFI_WPA_SUPPLICANT, PATH_ANDROID_WIFI_WPA_SUPPLICANT_BACKUP))
