
from behave import given, when, then, step
import traceback
import os
import sys

from time import sleep
from datetime import datetime

from pyand import ADB, Fastboot

from pprint import pprint

import subprocess, shlex
from threading import Timer

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_const import android_key_const



PATH_PC_LIB                                 = os.path.dirname(__file__)+'/../_lib/shell_script'
PATH_ANDROID_TEMP                           = r'/data/local/tmp'

FILE_TINKLABS1001                           = r'tinklabs1001'
FILE_CHANGE_SETTINGS                        = r'change_settings.sh'
FILE_CHANGE_PROP                            = r'change_prop.sh'

FILE_CHANGE_WPA_SUPPLICANT                  = r'change_wifi.sh'
FILE_WPA_SUPPLICANT                         = r'wpa_supplicant.conf'

PATH_PC_TINKLABS1001                        = '/'.join([PATH_PC_LIB, FILE_TINKLABS1001])
PATH_PC_CHANGE_SETTINGS                     = '/'.join([PATH_PC_LIB, FILE_CHANGE_SETTINGS])
PATH_PC_CHANGE_PROP                         = '/'.join([PATH_PC_LIB, FILE_CHANGE_PROP])

PATH_ANDROID_TINKLABS1001                   = '/'.join([PATH_ANDROID_TEMP, FILE_TINKLABS1001])
PATH_ANDROID_CHANGE_SETTINGS                = '/'.join([PATH_ANDROID_TEMP, FILE_CHANGE_SETTINGS])
PATH_ANDROID_CHANGE_PROP                    = '/'.join([PATH_ANDROID_TEMP, FILE_CHANGE_PROP])

PATH_PC_WPA_SUPPLICANT_CONF                 = '/'.join([PATH_PC_LIB, FILE_WPA_SUPPLICANT])
PATH_PC_CHANGE_WPA_SUPPLICANT               = '/'.join([PATH_PC_LIB, FILE_CHANGE_WPA_SUPPLICANT])
PATH_ANDROID_CHANGE_WPA_SUPPLICANT                    = '/'.join([PATH_ANDROID_TEMP, FILE_CHANGE_WPA_SUPPLICANT])


dParameters                                 = {}
dParameters['PATH_PC_LIB']                  = PATH_PC_LIB
dParameters['PATH_PC_TINKLABS1001']         = PATH_PC_TINKLABS1001
dParameters['PATH_PC_CHANGE_SETTINGS']      = PATH_PC_CHANGE_SETTINGS
dParameters['PATH_PC_CHANGE_PROP']          = PATH_PC_CHANGE_PROP

dParameters['PATH_PC_WPA_SUPPLICANT_CONF']  = PATH_PC_WPA_SUPPLICANT_CONF
dParameters['PATH_PC_CHANGE_WPA_SUPPLICANT']  = PATH_PC_CHANGE_WPA_SUPPLICANT

dParameters['PATH_ANDROID_TEMP']            = PATH_ANDROID_TEMP
dParameters['PATH_ANDROID_TINKLABS1001']    = PATH_ANDROID_TINKLABS1001
dParameters['PATH_ANDROID_CHANGE_SETTINGS'] = PATH_ANDROID_CHANGE_SETTINGS
dParameters['PATH_ANDROID_CHANGE_PROP']     = PATH_ANDROID_CHANGE_PROP

dParameters['PATH_ANDROID_CHANGE_WPA_SUPPLICANT']     = PATH_ANDROID_CHANGE_WPA_SUPPLICANT


# tinklabs-X555LNB% sudo fastboot -i 0x489 devices
# VZHGLMA750300169        fastboot

# fastboot oem fih on
# fastboot oem devlock key

# fastboot erase userdata
# fastboot erase oem

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

def get_epoch_time():
    """
        return the epoch of current time
    """
    return datetime.now().strftime('%s')


@step(u'ADB Wait for device')
def step_impl(context):
    if hasattr(context,'adb_session'):
        pass
    else:
        context.adb_session = ADB()

    adb=context.adb_session
    adb.run_cmd('wait-for-device')
    sleep(10)

@step(u'ADB Wait for device, timeout {sSeconds} seconds')
def step_impl(context, sSeconds):
    (iRetrunCode, sStdOut, sStdErr, bTimeout) = run('adb wait-for-device', timeout_sec=int(sSeconds))

    # wait some seconds more to let device ready
    sleep(10)

    pass

@step(u'ADB Reboot bootloader')
def step_impl(context):
    if hasattr(context,'adb_session'):
        pass
    else:
        logging.debug('create adb session')
        context.adb_session = ADB()

    adb=context.adb_session
    adb.run_cmd('reboot bootloader')
    sleep(10)


@step(u'ADB Reboot device')
def step_impl(context):
    """
        to be obsoleted, reboot device
    """
    if hasattr(context,'adb_session'):
        pass
    else:
        context.adb_session = ADB()

    adb=context.adb_session
    adb.run_cmd('reboot')
    sleep(10)

@step(u'ADB PATH_ANDROID_TEMP directory is ready, timeout {sSeconds} seconds')
def step_impl(context, sSeconds):
    iTimeToEnd = int(get_epoch_time())+ int(sSeconds)
    bDirectoryReady = False

    while iTimeToEnd > int(get_epoch_time()):
        (iReturnCode, sStdOut, sStdErr, bTimeout)=run('adb shell ls -l %s' % PATH_ANDROID_TEMP, timeout_sec=5)
        if iReturnCode == 0 :
            bDirectoryReady=True
            break

    if bDirectoryReady:
        pass
    else:
        print('Error: cannot get android temp direcotory')
        assert False

    pass

@step(u'ADB Initialize android')
def step_impl(context):
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
    adb = context.adb_session
    # adb.push_local_file(sSourceFile, sTargetFile)

    # adb.run_cmd('push %s %s' %(sSourceFile, sTargetFile))
    subprocess.check_output(
        'adb push %s %s' % (sSourceFile, sTargetFile)
        ,shell= True)

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
    print(u'STEP: Then ADB change permission change_wpa_supplicant')
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


@step(u'ADB adb shell test')
def step_impl(context):
    import subprocess
    adb = context.adb_session
    print('test command')
    # adb.run_cmd('shell "/data/local/tmp/tinklabs1001 -c \\"settings put global package_verifier_enable 0\\""')
    subprocess.check_output(
        'adb shell "/data/local/tmp/tinklabs1001 -c \\"settings put global package_verifier_enable 0\\""'
        ,shell= True)



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
    print('I am supposed to change the %s to %s' % (sSettingName, sValue))

    context.execute_steps(u'''
        Then ADB shell ""source /data/local/tmp/change_settings.sh put %s %s %s""
    ''' % ( sNamespace, sSettingName, sValue))
    pass


@step(u'ADB settings get {sNamespace} {sKey}')
def step_adb_settings_get(context, sNamespace, sKey):
    """
        a wrapper for adb settings get
    """

    return run('adb shell settings get %s %s' % (sNamespace, sKey), timeout_sec=5)


@step(u'ADB settings {sNamespace} {sKey} should be {sExpected}')
def step_adb_settings_compare(context, sNamespace, sKey, sExpected):
    """
        getting value from adb settings, with checking
    """
    (sReturnCode, sStdOut, sStdErr, sTimeout) = step_adb_settings_get(context, sNamespace, sKey)
    assert sExpected == sStdOut.strip()



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
    (sReturnCode, sStdOut, sStdErr, sTimeout) = step_adb_getprop(context, sName)
    print('props returned: %s' % sStdOut.strip())
    assert sExpected == sStdOut.strip()

@step(u'ADB setprop test with shell True')
def step_impl(context):
    print(u'STEP: Given ADB setprop test with shell True')
    context.execute_steps(u'''
        Given ADB Init session
            And ADB push tinklabs1001
            And ADB push change_prop

        Then ADB change permission tinklabs1001
            And ADB change permission change_prop

    ''')
    pprint(run('''adb shell "echo 0 > /sys/class/android_usb/f_mtp/device/f_mass_storage/enable"''', timeout_sec=5))


@step(u'ADB disable usb mass storage')
def step_disable_usb_mass_storage(context):
    """
        disable usb mass storage function on the device
    """
    print('STEP: disable usb mass storage')
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
        dParameter['sTargetPathWithDatetime'] = os.path.join(dParameter['sTargetPath'], dParameter['sEpoch'])

        lsADBCommand=[]
        lsADBCommand.append('shell screencap -p /sdcard/%(sEpoch)s.png' % dParameter)
        lsADBCommand.append('pull /sdcard/%(sEpoch)s.png %(sTargetPathWithDatetime)s' % dParameter)
        lsADBCommand.append('shell rm /sdcard/%(sEpoch)s.png' % dParameter)
        lsADBCommand.append('shell uiautomator dump')
        lsADBCommand.append('pull /sdcard/window_dump.xml %(sTargetPathWithDatetime)s/dump.uix' % dParameter)
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
    proc = subprocess.Popen(shlex.split(sCommand), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


@step(u'ADB shell "{sCommand}"')
def step_adb_shell(context, sCommand):
    """
        debug command

        :Args:
            - sEventCode - key event code given by 3 -->  "KEYCODE_HOME"
    """
    sAdbCommand = 'adb shell %s' % sCommand
    print('i am supposed to run adb command %s' % sAdbCommand)
    (iResultCode, sStdOut, sStdErr, bTimeout) = run(sAdbCommand, timeout_sec = 5)
    return


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

    iTimeToEnd = int(get_epoch_time()) + int(sSeconds)

    # for i in range(0, int(sSeconds)):
    while iTimeToEnd > int(get_epoch_time()):
        sleep(15)
        (sResultCode, sStdOut, sStdErr, bTimeout) = step_adb_getprop(context, "sys.boot_completed")
        sStdOut = sStdOut.strip()

        if sStdOut == '1':
            bBootComplete = True
            break

    if bBootComplete:
        pass
    else:
        print('boot failed')
        print("sStdOut: %s" % sStdOut)
        assert False


# global options:
#  -a         listen on all network interfaces, not just localhost
#  -d         use USB device (error if multiple devices connected)
#  -e         use TCP/IP device (error if multiple TCP/IP devices available)
#  -s SERIAL
#      use device with given serial number (overrides $ANDROID_SERIAL)
#  -p PRODUCT
#      name or path ('angler'/'out/target/product/angler');
#      default $ANDROID_PRODUCT_OUT
#  -H         name of adb server host [default=localhost]
#  -P         port of adb server [default=5037]
#  -L SOCKET  listen on given socket for adb server [default=tcp:localhost:5037]

# general commands:
#  devices [-l]             list connected devices (-l for long output)
#  help                     show this help message
#  version                  show version num

# networking:
#  connect HOST[:PORT]      connect to a device via TCP/IP [default port=5555]
#  disconnect [HOST[:PORT]]
#      disconnect from given TCP/IP device [default port=5555], or all
#  forward --list           list all forward socket connections
#  forward [--no-rebind] LOCAL REMOTE
#      forward socket connection using:
#        tcp:<port> (<local> may be "tcp:0" to pick any open port)
#        localabstract:<unix domain socket name>
#        localreserved:<unix domain socket name>
#        localfilesystem:<unix domain socket name>
#        dev:<character device name>
#        jdwp:<process pid> (remote only)
#  forward --remove LOCAL   remove specific forward socket connection
#  forward --remove-all     remove all forward socket connections
#  ppp TTY [PARAMETER...]   run PPP over USB
#  reverse --list           list all reverse socket connections from device
#  reverse [--no-rebind] REMOTE LOCAL
#      reverse socket connection using:
#        tcp:<port> (<remote> may be "tcp:0" to pick any open port)
#        localabstract:<unix domain socket name>
#        localreserved:<unix domain socket name>
#        localfilesystem:<unix domain socket name>
#  reverse --remove REMOTE  remove specific reverse socket connection
#  reverse --remove-all     remove all reverse socket connections from device

# file transfer:
#  push LOCAL... REMOTE
#      copy local files/directories to device
#  pull [-a] REMOTE... LOCAL
#      copy files/dirs from device
#      -a: preserve file timestamp and mode
#  sync [DIR]
#      copy all changed files to device; if DIR is "system", "vendor", "oem",
#      or "data", only sync that partition (default all)
#      -l: list but don't copy

# shell:
#  shell [-e ESCAPE] [-n] [-Tt] [-x] [COMMAND...]
#      run remote shell command (interactive shell if no command given)
#      -e: choose escape character, or "none"; default '~'
#      -n: don't read from stdin
#      -T: disable PTY allocation
#      -t: force PTY allocation
#      -x: disable remote exit codes and stdout/stderr separation
#  emu COMMAND              run emulator console command

# app installation:
#  install [-lrtsdg] PACKAGE
#  install-multiple [-lrtsdpg] PACKAGE...
#      push package(s) to the device and install them
#      -l: forward lock application
#      -r: replace existing application
#      -t: allow test packages
#      -s: install application on sdcard
#      -d: allow version code downgrade (debuggable packages only)
#      -p: partial application install (install-multiple only)
#      -g: grant all runtime permissions
#  uninstall [-k] PACKAGE
#      remove this app package from the device
#      '-k': keep the data and cache directories

# backup/restore:
#  backup [-f FILE] [-apk|-noapk] [-obb|-noobb] [-shared|-noshared] [-all] [-system|-nosystem] [PACKAGE...]
#      write an archive of the device's data to FILE [default=backup.adb]
#      package list optional if -all/-shared are supplied
#      -apk/-noapk: do/don't back up .apk files (default -noapk)
#      -obb/-noobb: do/don't back up .obb files (default -noobb)
#      -shared|-noshared: do/don't back up shared storage (default -noshared)
#      -all: back up all installed applications
#      -system|-nosystem: include system apps in -all (default -system)
#  restore FILE             restore device contents from FILE

# debugging:
#  bugreport [PATH]
#      write bugreport to given PATH [default=bugreport.zip];
#      if PATH is a directory, the bug report is saved in that directory.
#      devices that don't support zipped bug reports output to stdout.
#  jdwp                     list pids of processes hosting a JDWP transport
#  logcat                   show device log (logcat --help for more)

# security:
#  disable-verity           disable dm-verity checking on userdebug builds
#  enable-verity            re-enable dm-verity checking on userdebug builds
#  keygen FILE
#      generate adb public/private key; private key stored in FILE,
#      public key stored in FILE.pub (existing files overwritten)

# scripting:
#  wait-for[-TRANSPORT]-STATE
#      wait for device to be in the given state
#      State: device, recovery, sideload, or bootloader
#      Transport: usb, local, or any [default=any]
#  get-state                print offline | bootloader | device
#  get-serialno             print <serial-number>
#  get-devpath              print <device-path>
#  remount
#      remount /system, /vendor, and /oem partitions read-write
#  reboot [bootloader|recovery|sideload|sideload-auto-reboot]
#      reboot the device; defaults to booting system image but
#      supports bootloader and recovery too. sideload reboots
#      into recovery and automatically starts sideload mode,
#      sideload-auto-reboot is the same but reboots after sideloading.
#  sideload OTAPACKAGE      sideload the given full OTA package
#  root                     restart adbd with root permissions
#  unroot                   restart adbd without root permissions
#  usb                      restart adb server listening on USB
#  tcpip PORT               restart adb server listening on TCP on PORT

# internal debugging:
#  start-server             ensure that there is a server running
#  kill-server              kill the server if it is running
#  reconnect                kick connection from host side to force reconnect
#  reconnect device         kick connection from device side to force reconnect

# environment variables:
#  $ADB_TRACE
#      comma-separated list of debug info to log:
#      all,adb,sockets,packets,rwx,usb,sync,sysdeps,transport,jdwp
#  $ADB_VENDOR_KEYS         colon-separated list of keys (files or directories)
#  $ANDROID_SERIAL          serial number to connect to (see -s)
#  $ANDROID_LOG_TAGS        tags to be used by logcat (see logcat --help)
