#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging

from behave import given, when, then, step
from common import *
import subprocess

from config import *
from pyand import ADB, Fastboot

from collections import deque

from time import sleep

# appium and android
# https://github.com/appium/python-client
from appium import webdriver
from pyand import ADB, Fastboot

# android stuff
import android_capabilities

sys.path.append(os.path.dirname(__file__) + '/../_lib')
from android_function import finger

from android_const import android_key_const
from android_const import android_os_permission_button

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction


from devices import *

from appium_function import *


def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

def bootstrap_from_unknown_state(android_serial):
    """ for handle the device at the very beginnibng
        I would like to make the device printable from "adb devices" while escape from this loop

    Args:
        android_serial: the serial number of android

    NOTES/IDEAS:
        to guide the device incase the device is trapped into the fastboot mode.
    """

    keep_loop = True
    countdown = 10

    try:
        while keep_loop and countdown > 0:
            print('countdown remains for bootstrap :%d' % countdown)
            countdown -= 1
            sleep(1)
            adb_devices_output = subprocess.check_output(['adb', 'devices'])
            if adb_devices_output.find(android_serial) > -1:
                # if the device serial is found from adb devices output, escape from the loop
                print('device appears in the adb devices result')
                keep_loop = False
                pass
            else:
                # if the device serial cannot found from adb devices output
                # possibly the device is in the bootloader mode, fastboot -> reboot the device to recover
                print('device not appears in the adb devices result')

                # TODO: consider remove me
                from pprint import pprint
                print('dump the value of: adb_devices_output')
                pprint(adb_devices_output)

                fastboot_output = subprocess.check_output(['fastboot', 'devices'])
                if fastboot_output.find(android_serial) > -1:
                    print('devices appears in the fastboot devices result')
                    subprocess.check_output(
                        ['fastboot', '-s', android_serial, 'reboot'])
                    sleep(90)
                else:
                    print('devices not appears int the fastboot devices result')

                    # TODO: consider remove me
                    from pprint import pprint
                    print('dump the value of: fastboot_output')
                    pprint(fastboot_output)

        pass
    except Exception as e:
        print('error found during bootstrap from unknown state')
        print('is the android_serial number correct ?')


        # TODO: remove me
        from pprint import pprint
        print('dump the value of: android_serial')
        pprint(android_serial)

        print('dump the value of: adb_devices_output')
        pprint(adb_devices_output)

        print('dump the value of: fastboot_output')
        pprint(fastboot_output)


        raise e
    else:
        pass


@step(u'Target device is {device} "{android_serial}"')
def step_impl(context, device, android_serial):
    """specify android device by model and serial number

    Args:
        - device [T1, M812]
        - android_serial  V2HGLMB721301100
    Assumption:
        The device is in normal state with ADB ready
    """

    # STEP: start setting up target
    print("STEP: start setting up target")

    try:
        context.device = device
        context.android_serial = android_serial.encode('ascii', 'ignore')

        bootstrap_from_unknown_state(android_serial)

        temp_adb = ADB()
        temp_fastboot = Fastboot()

        list_by_serial = {
            serial: idx
            for (idx, serial) in temp_adb.get_devices().items()
        }

        if android_serial in list_by_serial.keys():

            target_id = list_by_serial[android_serial]
            temp_adb.set_target_by_id(target_id)

            context.adb_session = temp_adb
            context.fastboot_session = temp_fastboot

        else:
            print_fail('cannot find the target device')
            assert False, 'cannot find the target device'

        pass
    except Exception as e:
        print('error occur during finding the target device')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: device')
        pprint(device)

        print('dump the value of: android_serial')
        pprint(android_serial)
        # TODO: remove me

        raise e
    else:
        pass

    # NOTE: load class device config here
    if device in ['T1']:
        context.device_config = Device_T1
    elif device in ['M812']:
        context.device_config = Device_M812
    else:
        assert False, 'device configuration is missing device.py'


@step(u'Target device is {device}')
def step_impl(context, device):
    """
    Setup context for a device, initiate ADB and fastboot for later use

    Args:
        device: the model of the device

    """
    try:
        context.device = device
        context.adb_session = ADB()
        context.fastboot_session = Fastboot()
        pass
    except Exception as e:
        print('error occur during finding target device')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: device')
        pprint(device)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'{process_wanted} is running')
def step_impl(context, process_wanted):
    """
    Assert if the process wanted is not running

    Args:
        process_wanted: the process wanted
    """

    try:
        if os.popen("ps -ef | grep -i %s | grep -v 'grep'" % process_wanted).read().strip().find(process_wanted) > -1:
            print('running %s found' % process_wanted)
            pass
        else:
            assert False, 'the wanted application %s is not running' % process_wanted
    except Exception, e:
        print('cannot find the wanted process %s' % process_wanted)
        # print('the wanted application %s is not running ' %
        #               process_wanted)
        assert False, 'exception raised during catching the wanted application'


@step(u'setup an android as below, using appium port {port}')
def step_impl(context, port):
    try:
        row = context.table[0]

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = row['version']

        print('setting up appium process')

        if hasattr(context, 'android_serial') and len(context.android_serial) == 16:
            desired_caps['deviceName'] = context.android_serial
            print('context.android_serial defined, use as deviceName')

            desired_caps['udid'] = context.android_serial
            print('context.android_serial defined, use as udid')

        else:
            desired_caps['deviceName'] = 'Android'
            print(
                'context.android_serial not defined, use "Android" as deviceName')

        # desired_caps['app'] = row['PATH(packageName)']
        desired_caps['appPackage'] = row['Package']
        desired_caps['appActivity'] = row['Activity']
        desired_caps['appWaitActivity'] = row['Activity']
        desired_caps['deviceReadyTimeout'] = 30
        desired_caps['noReset'] = True

        # NOTE: using UiAutomator2 increase capataibility
        desired_caps['automationName'] = 'UiAutomator2'

        # provision of more than 1 session there, so the context_port is a list
        # context.appiumSession = webdriver.Remote(
        #     'http://localhost:%d/wd/hub' % context.appium_port[0],
        #     desired_caps)

        # TODO: remove me
        context.appiumSession = webdriver.Remote(
            'http://localhost:%d/wd/hub' % int(port),
            desired_caps)
        print('setup appium done')
    except Exception as e:
        print('cannot connect to the appium')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: port')
        pprint(port)
        # TODO: remove me

        raise e
    else:
        pass

@step(u'setup an android as below')
def step_impl(context):
    row = context.table[0]

    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    # desired_caps['platformVersion'] = row['version']

    if hasattr(context, 'android_serial') and len(context.android_serial) == 16:
        desired_caps['deviceName'] = context.android_serial
    else:
        desired_caps['deviceName'] = 'Android'

    # desired_caps['app'] = row['PATH(packageName)']
    desired_caps['appPackage'] = row['Package']
    desired_caps['appActivity'] = row['Activity']
    desired_caps['deviceReadyTimeout'] = 30
    desired_caps['noReset'] = False

    # provision of more than 1 session there, so the context_port is a list
    # context.appiumSession = webdriver.Remote(
    #     'http://localhost:%d/wd/hub' % context.appium_port[0],
    #     desired_caps)

    # TODO: remove me
    context.appiumSession = webdriver.Remote(
        'http://localhost:4723/wd/hub', desired_caps)


@given('started package "{packageName}" activity "{sActivity}" on "{sPlatform}" type "{sType}" ver "{sVersion}"')
def step_impl(context, packageName, sActivity, sType, sPlatform, sVersion):
    try:

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        # TODO: remove me
        # desired_caps['platformVersion'] = sVersion
        desired_caps['deviceName'] = 'Android'
        desired_caps['appPackage'] = packageName
        desired_caps['appActivity'] = sActivity
        desired_caps['deviceReadyTimeout'] = 30
        desired_caps['noReset'] = False

        # output a appiumSession for latter use
        context.appiumSession = webdriver.Remote(
            'http://localhost:4723/wd/hub', desired_caps)
    except Exception as e:
        print('error occur during start package and activity')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: packageName')
        pprint(packageName)

        print('dump the value of: sActivity')
        pprint(sActivity)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'sleep {n} seconds')
def step_impl(context, n):
    """
    sleep for a given time

    Args:
        n: n in seconds

    # NOTE: try to unify the sleep in following list
        # sleep 1 seconds
        # sleep 5 seconds
        # sleep 15 seconds
        # sleep 30 seconds
        # sleep 60 seconds
    """
    sleep(int(n))


@step(u'halt myself')
def step_impl(context):
    """
        sleep long enough for troubleshoot purpose
        # NOTE: for debug use
    """
    sleep(99999)


# com.tinklabs.launcher.apk
@step(u'User tap on "{button}" button')
def step_impl(context, button):
    """
    simiulate user tap on android button by text

    Args:
        button: the text on the button
    """
    try:
        finger.f_FindButtonWithText(context.appiumSession, button)[0].click()
        pass
    except Exception as e:
        print('error occur while trying to tap on button %s' % button)
        raise e
    else:
        pass


# @then(u'Fail if "{component}", "{activity}" not active')
# def step_impl(context, component, activity):
#     """check the active android activity on screen"""
#     if component + '/' + activity != finger.f_CheckCurrentActivity(context.appiumSession):
#         assert False

@step(u'adb binary is available')
def step_impl(context):
    """
    assert the adb binary is available
    """
    try:
        if os.path.isfile(context.adb_binary):
            print('adb binary found')
            pass
        else:
            assert False, '%s is not exist' % context.adb_binary
    except Exception as e:
        print('error occur during locating the adb binary')
        raise e
    else:
        pass


@step(u'Test setup is ready')
def step_impl(context):
    try:
        context.execute_steps(u'''
        Given adb binary is available
        Given appium is running

          Given Fastboot init
          Given FASTBOOT Erase userdata
            And ADB Wait for device, timeout 600 seconds

            # about 600 for T1
            # about 900 for M812
            And ADB check boot completed, timeout 1200 seconds

        Then Wait for handy initialization
            # TODO: resume
            # And inject wifi configuration WIFI_CONFIG_TINKLABS_WTTQA
            And ADB Initialize android
        ''')
        pass
    except Exception as e:
        print('error occur during checking Test setup is ready')
        raise e
    else:
        pass


@step(u'quit appium')
def quit_appium(context):
    try:
        if hasattr(context, 'appiumSession'):
            context.appiumSession.quit()
    except Exception as e:
        print('error occur during quit appium')
        raise e
    else:
        pass


@step(u'Find "{Text}" on screen')
def find_text_on_screen(context, Text):
    els =[]
    try:
        els = finger.f_FindTargetByXPath(
            context.appiumSession,
            "android.widget.TextView", "text", Text
        )
    except Exception as e:
        print('error occur during try to locate the text %s on screen ' % Text)
        raise e
    else:
        pass

    return els


@step(u'Find "{sId}" on screen, timeout {sTimeout} seconds')
def find_recourceid_on_screen_with_timeout(context, sId, sTimeout):
    """
        loop until the element available on screen. return the elements found.
    """

    els = []
    try:
        for i in range(1, int(sTimeout) + 1):
            sleep(1)
            els = finger.f_FindTargetById(
                context.appiumSession,
                sId
            )
            if len(els) > 0:
                break
        pass
    except Exception as e:
        print('error occur during finding resource-id on screen')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sId')
        pprint(sId)
        # TODO: remove me

        raise e
    else:
        pass


    return els


@step(u'Wait "{sId}" on screen, timeout {sTimeout} seconds')
def wait_recourceid_on_screen_with_timeout(context, sId, sTimeout):
    """
        loop until the element not appears on screen, assume the element is already on screen.
    """
    els = []
    try:
        for i in range(1, int(sTimeout) + 1):
            sleep(1)
            els = finger.f_FindTargetById(
                context.appiumSession,
                sId
            )
            if len(els) < 1:
                break

    except Exception as e:
        print('error occur while try to find the sId %s on screen ' % sId)

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sId')
        pprint(sId)
        # TODO: remove me

        raise e
    else:
        pass

    return els


@step(u'Wait until screen ready, timeout {ready_timeout} seconds')
def step_impl(context, ready_timeout):
    """
        Wait until screen is ready for click
        current definition:
            - all loading bar gone, TBA
    """
    # Resource-id com.tinklabs.launcher:id/loading

    try:

        iTimeout = int(ready_timeout)
        dqiElementFound = deque([1, 1, 1])

        for i in range(1, iTimeout):
            sleep(1)
            dqiElementFound.popleft()
            dqiElementFound.append(
                len(wait_recourceid_on_screen_with_timeout(
                    context, "com.tinklabs.launcher:id/loading", '1'))
            )

            if not(any(dqiElementFound)):
                break

        # if any(dqiElementFound):
        #     print('screen keeps busy in %s seconds' % ready_timeout)
        #     # assert False

        pass
        print('suppose screen is ready')
    except Exception as e:
        print('the screen not ready within timeout value %d' % ready_timeout)
        raise e
    else:
        pass

    pass


@step(u'Fail if the "{Text}" not appears on screen')
def fail_if_the_text_not_appears(content, Text):
    try:
        lLookFor = find_text_on_screen(content, Text)
        if isinstance(lLookFor, list) and len(lLookFor) == 1:
            pass
        else:
            assert False, 'the unwanted text is appearing'
        pass
    except Exception as e:
        print('error occur during try to locate the text on screen or unwanted text is appearing')
        print('the text wanted doesnt appear')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: Text')
        pprint(Text)
        # TODO: remove me

        raise e
    else:
        pass


# @step(u'Fail if the button "{sText}" not appears')


@step(u'Fail if the button "{Text}" not appears on screen')
def step_impl(context, Text):
    """
        find the button/textview by the text given by Text
        assert fail if nothing found
    """
    try:
        lLookFor = finger.f_FindButtonWithText(
            context.appiumSession, Text
        )

        if isinstance(lLookFor, list) and len(lLookFor) == 1:
            pass
        else:
            print(lLookFor)
            assert False, 'the Text is not appearing on screen'
        pass
    except Exception as e:
        print('error occur while locating the Text %s ' % Text)
        raise e
    else:
        pass


@step(u'Fail if the Text "{sText}" {sDetermin} appears on screen')
def step_impl(context, sText, sDetermin):
    """
        find the textview by the text given by Text
        decision made by sDetermin
            1. sDetermin = is , the False assertion applied when text found on screen
            2. sDetermin = not, the False assertion applied when text not found on screen
    """
    try:
        context.execute_steps(u'''
            Then Wait until screen ready, timeout 60 seconds
        ''')

        lLookFor = finger.f_FindElementsWithText(
            context.appiumSession, sText
        )

        if isinstance(lLookFor, list) and len(lLookFor) > 0:
            # NOTE the text found which is unwanted
            if sDetermin in ['is']:
                assert False, ' Failed as the wanted text is appearing on screen'
        else:
            # NOTE the text not found which is wanted
            if sDetermin in ['not']:
                assert False, ' Failed as the unwanted text is appearing on screen'

        pass
    except Exception as e:
        print(
            'error occur during the Fail if the Text appears on screen')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sText')
        pprint(sText)

        print('dump the value of: sDetermin')
        pprint(sDetermin)

        print('dump the value of: lLookFor')
        pprint(lLookFor)


        raise e
    else:
        pass


@step(u'Check if the {sText} appears on screen')
def step_impl(context, sText):
    els=0
    try:
        els = len(finger.f_FindElementsWithText(
            context.appiumSession, sText
        ))

        pass
    except Exception as e:
        print('error occur during checking if the text appears on screen')


        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: sText')
        pprint(sText)


        raise e
    else:
        pass

    return els


@step(u'Fail if the resources-id"{sId}" not appears')
def step_impl(context, sId):
    """
        NOTE: debug function for llaw
    """
    try:
        lLookFor = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )

        if isinstance(lLookFor, list) and len(lLookFor) == 1:
            pass
        else:
            assert False, ' Failed as the resources-id"{sId}" not appears'
        pass
    except Exception as e:
        print('error occur during trying to located the sId')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: sId')
        pprint(sId)

        raise e
    else:
        pass


@step(u'Wait until "resource-id" "{sId}" appears on screen, timeout {sTimeout} seconds')
def step_impl(context, sId, sTimeout):
    """
    Try to locate sId on current screen, timeout given by sTimeout
    e.g.:
        Wait until "resource-id" "com.tinklabs.launcher:id/ivBackground" appears on screen, timeout 60 seconds

    :Args:
        - sId - recource-id
        - sTimeout - timeout second
    # TODO: replace com.tinklabs.launcher:id/ivBackground using meaningful name
    """
    try:
        lLookFor = []

        start_time = get_epoch_time()
        end_time = start_time + int(sTimeout)

        print('try to unlock screen')
        context.execute_steps(u'''
            Then appium unlock screen
        ''')

        while end_time > get_epoch_time():

            sleep(1)
            lLookFor = finger.f_FindTargetById(
                context.appiumSession,
                sId
            )

            if len(lLookFor) > 0:
                break

        if len(lLookFor) > 0:
            pass
        else:
            assert False, 'cannot find expected resource'
        pass
    except Exception as e:
        print('error occur during try to locate the sId on screen ')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sId')
        pprint(sId)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'Wait until Video"{sId}" appears, timeout {sTimeout} seconds')
def step_impl(context, sId, sTimeout):
    try:
        lLookFor = []

        print('try to unlock screen')
        context.execute_steps(u'''
            Then appium unlock screen
        ''')

        for i in range(1, int(sTimeout) + 1):

            sleep(1)
            lLookFor = finger.f_FindTargetById(
                context.appiumSession,
                sId
            )

            if len(lLookFor) > 0:
                break

        if len(lLookFor) > 0:
            pass
        else:
            assert False, 'error occur during try to locate the sId for Video'

        pass
    except Exception as e:
        print('error occur during try to locate the sId for Video')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sId')
        pprint(sId)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'Fail if the Video"{sId}" not appears')
def step_impl(context, sId):
    try:
        lLookFor = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )

        if isinstance(lLookFor, list) and len(lLookFor) > 0:
            pass
        else:
            assert False, ' Failed as the Video not appears'
        pass
    except Exception as e:
        print('error occur while try to locate the Video:sId')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sId')
        pprint(sId)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'tap screen {n} times at {somewhere}')
def step_impl(context, n, somewhere):
    """just tap on a position defined"""

    try:
        finger.f_TapScreen(context.appiumSession, 1, 1, 1)
        pass
    except Exception as e:
        print('error occur during try to tap the screen')
        raise e
    else:
        pass


@step(u'tap on Text "{sText}"')
def step_impl(context, sText):
    """
    wait until screen ready, tap on the element by its text

    Args:
        sText: the text wanted to tap

    """
    try:
        context.execute_steps(u'''
            Then Wait until screen ready, timeout 30 seconds
        ''')

        els = finger.f_FindElementsWithText(
            context.appiumSession, sText
        )
        if els:
            sleep(1)
            els[0].click()

        else:
            print('cannot find the wanted text')
            assert False, 'cannot find the wanted text: %s' % sText
        pass
    except Exception as e:
        print('error occur during try to want until the screen is ready')


        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sText')
        pprint(sText)
        # TODO: remove me

        raise e
    else:
        pass



@step(u'press "{dPadKey}" button')
def step_impl(context, dPadKey):
    try:
        finger.f_PressKey(context.appiumSession, dPadKey)
        pass
    except Exception as e:
        print('error during pressing button')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: dPadKey')
        pprint(dPadKey)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'press {ButtonName} button')
def step_impl(context, ButtonName):
    try:
        if ButtonName == 'HOME':
            finger.f_PressKey(context.appiumSession, android_key_const.HOME)
        pass
    except Exception as e:
        print('error pressing button')


        # TODO: remove me
        from pprint import pprint
        print('dump the value of: ButtonName')
        pprint(ButtonName)
        # TODO: remove me

        raise e
    else:
        pass


@step(u'tap on button "{sWidget}":"{sProperties}":"{sDescription}"')
def step_impl(context, sWidget, sProperties, sDescription):
    try:
        context.execute_steps(u'''
            Given Wait until screen ready, timeout 60 seconds
        ''')
        finger.f_TapWidgetByPropertiesAndValue(
            context.appiumSession,
            sWidget, sProperties, sDescription)
        sleep(1)
        pass
    except Exception as e:
        print('error during tapping button')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sWidget')
        pprint(sWidget)
        # TODO: remove me

        raise e
    else:
        pass
    pass


@step(u'tap on checkbox "{sWidget}":"{sProperties}":"{sDescription}"')
def step_impl(context, sWidget, sProperties, sDescription):
    try:
        finger.f_TapWidgetByPropertiesAndValue(
            context.appiumSession,
            sWidget, sProperties, sDescription)
        sleep(1)
        pass
    except Exception as e:
        print('error during tapping the checkbox')
        raise e
    else:
        pass
    pass


# and Fail if the activity "com.tinklabs.launcher.features.main.activity.LauncherActivity" not active in "10" seconds
@step(u'Fail if the activity "{sActivity}" not active in "{sSeconds}" seconds')
def step_impl(context, sActivity, sSeconds):
    """
        wrapper for appium wait_activity
    """
    try:
        bResult = finger.f_waitForActivity(
            context.appiumSession,
            sActivity,
            int(sSeconds)
        )

        if bResult:
            pass
        else:
            print('cannot find activity %s' % sActivity)
            assert False
        pass
    except Exception as e:
        raise e
    else:
        pass


@step(u'tap on position "{sX}","{sY}" using adb')
def step_impl(context, sX, sY):
    """
        tap on specific position
        TODO: handle this using appium. unknown temporary solution
    """

    # sTapCmd = "adb shell input tap %s %s" % (sX, sY)
    # lCmd = sTapCmd.split(' ')
    # subprocess.check_output(lCmd)
    try:
        # print('adb tap on screen position %s, %s' % (sX, sY))
        context.adb_session.run_cmd('shell input tap %s %s' % (sX, sY))
        pass
    except Exception as e:
        print('error found during tapping screen to keep awake using adb')
        raise e
    else:
        pass

    pass


@then(u'Fail if the content-desc "{sText}" {sDetermine} appears on screen')
def step_impl(context, sText, sDetermine):
    try:
        els = finger.f_FindElementsWithContentDesc(context.appiumSession, sText)

        if els:
            # NOTE content-desc appears on screen
            if sDetermine in ['is']:
                assert False, 'the unwanted elements %s appears on screen' % sText
        else:
            if sDetermine in ['not']:
                assert False, 'the wanted elements %s not appears on screen' % sText
        pass
    except Exception as e:
        print('error found during finding if the context-desc appears on screen')
        raise e
    else:
        pass

    pass


def get_free_port(port_range):
    """
        slice to catch the free port from host
        Args:
            - port_range - list of port to be probed

        returns:
            a free port, -1 if not found
    """

    import random
    import socket

    result = -1
    try:

        free_port_found = False
        random.shuffle(port_range)

        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 2 Second Timeout
            if sock.connect_ex(('0.0.0.0', port)) == 61:
                # port is free
                free_port_found = True
                result = port
                break
            else:
                pass

        if free_port_found:
            pass
        else:
            print('cannot find free port for appium')
            assert False, 'cannot find free port for appium'
        pass
    except Exception as e:
        print('error during finding a freeport for appium')
        raise e
    else:
        pass

    return result


@step(u'noop')
def step_impl(context):
    print('i am supposed no operation, just an print out only')


@given(u'a new working directory')
def step_impl(context):
    logging.info(u'STEP: Given a new working directory')


@given(u'a file named "{filename}" with')
def step_impl(context, filename):
    try:
        print(u'STEP: create file with content')

        f = open(filename, 'w')
        f.write(context.text)
        f.close()
        pass
    except Exception as e:
        raise e
    else:
        pass


@given(u'start appium')
def step_impl(context):
    """
    try to initiate the appium by behave.
    port number is picken by random
    udid (serial number on android) is by the context.android_serial
    """
    print(u'STEP: Given start appium')

    try:
        appium_port = get_free_port(range(4723, 4723 + 999))

        # NOTE: using 1 on 1 strategy, currently supposed the number of appium session is same as the number of device attached

        appium_command = PATH_APPIUM_BINARY + \
            ' -U %s --port %d' % (context.android_serial, appium_port)
        print('android_serial:%s' % context.android_serial)
        print('appium_port:%d' % appium_port)
        print("appium_command: %s" % appium_command)

        appium_process = subprocess.Popen(
            appium_command.split(' '), stdout=subprocess.PIPE
        )
        print(appium_command)

        # TODO: remove me
        # context.appiumSession = webdriver.Remote(
        #     'http://localhost:4723/wd/hub',
        #     desired_caps)
        context.appium_port.append(appium_port)
        context.appium_pid.append(appium_process.pid)

        # wait some seconds for appium start
        sleep(5)
        pass
    except Exception as e:
        raise e
    else:
        pass


@step(u'stop appium')
def step_impl(context):
    print(u'STEP: stop appium')

    try:
        # TODO: move me up
        import psutil

        for pid in context.appium_pid:
            os.kill(pid, signal.SIGTERM)
        pass
    except Exception as e:
        raise e
    else:
        pass


@given(u'setup android appium demo app')
def step_impl(context):
    try:
        print(u'STEP: Given setup android appium demo app')

        desired_caps = {}
        desired_caps['platformName'] = 'android'
        # desired_caps['platformVersion'] = '7.0'
        desired_caps['deviceName'] = 'VZHGLMA742804186'
        desired_caps['app'] = PATH(
            '/Users/louis_law/.android_tinklabs/ApiDemos-debug.apk'
        )

        context.appium_session = webdriver.Remote(
            'http://localhost:%s/wd/hub' % context.appium_port[0], desired_caps)
        pass
    except Exception as e:
        print('error while setup android appium demo app')
        raise e
    else:
        pass


@step(u'test appium screen capture')
def step_impl(context):

    try:
        screen_capture = appium_screen_capture(context.appiumSession, '/Users/louis_law')
        screen_capture.capture_failed_screen()
        pass
    except Exception as e:
        print('error occur while capture the screen by appium')
        raise e
    else:
        pass


@step(u'appium screen capture, save file to path "{pathname}"')
def step_impl(context, pathname):
    try:
        screen_capture = appium_screen_capture(
            context.appiumSession, pathname)
        screen_capture.capture_failed_screen()

    except Exception as e:
        print('error occur while capture the screen by appium')

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: pathname')
        pprint(pathname)
        # TODO: remove me

        raise e
    else:
        pass

@step(u'appium capture failed screen')
def step_impl(context):
    try:
        # TODO: remporary hardcode for the model
        print('capture failure screen invoked')
        print('saving to directory: %s' % context.device_config.PATH_FAILURE_SCREEN_CAPTURE)
        screen_capture = appium_screen_capture(
            context.appiumSession, context.device_config.PATH_FAILURE_SCREEN_CAPTURE
        )
        screen_capture.capture_failed_screen()

        pass
    except Exception as e:
        print('error during appium capture failed screen')
        raise e
    else:
        pass


@step(u'appium unlock screen')
def step_impl(context):
    try:
        context.execute_steps(u'''
            Then ADB shell "am start -n io.appium.unlock/.Unlock"
        ''')
        pass
    except Exception as e:
        print('error during appium unlock screen')
        raise e
    else:
        pass
