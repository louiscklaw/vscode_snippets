#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

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


def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


@step(u'Target device is {device} "{android_serial}"')
def step_impl(context, device, android_serial):
    """
        specify android device by model and serial number
        Args:
            - device [T1, M812]
            - android_serial  V2HGLMB721301100
    """
    context.device = device
    context.android_serial = android_serial.encode('ascii', 'ignore')

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
    context.device = device
    context.adb_session = ADB()
    context.fastboot_session = Fastboot()


@step(u'{process_wanted} is running')
def step_impl(context, process_wanted):
    """
    Assert if the process wanted is not running

    Args:
        process_wanted: the process wanted
    """
    try:
        if os.popen("ps -ef | grep -i %s | grep -v 'grep'" % process_wanted).read().strip().find(process_wanted) > -1:
            pass
        else:
            assert False, 'the wanted application %s is not running' % process_wanted
    except Exception, e:
        # logging.error('the wanted application %s is not running ' %
        #               process_wanted)
        assert False, 'exception raised during catching the wanted application'


@step(u'setup an android as below, using appium port {port}')
def step_impl(context, port):
    row = context.table[0]

    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    # desired_caps['platformVersion'] = row['version']

    if hasattr(context, 'android_serial') and len(context.android_serial) == 16:
        desired_caps['deviceName'] = context.android_serial
        logging.debug('context.android_serial defined, use as deviceName')

        desired_caps['udid'] = context.android_serial
        logging.debug('context.android_serial defined, use as udid')

    else:
        desired_caps['deviceName'] = 'Android'
        logging.debug(
            'context.android_serial not defined, use "Android" as deviceName')

    # desired_caps['app'] = row['PATH(packageName)']
    desired_caps['appPackage'] = row['Package']
    desired_caps['appActivity'] = row['Activity']
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

    # desired_caps = {}
    # desired_caps['platformName'] = 'Android'
    # desired_caps['platformVersion'] = '7.0'
    # desired_caps['deviceName'] = 'test device'

    # desired_caps['deviceName'] = 'Android Emulator'
    # desired_caps['app'] = '/Users/louis_law/Documents/_workspace/handy_appium/_apk/ApiDemos-debug.apk'

    # self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


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
    finger.f_FindButtonWithText(context.appiumSession, button)[0].click()


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
    if os.path.isfile(context.adb_binary):
        pass
    else:
        assert False, '%s is not exist' % context.adb_binary


@step(u'Test setup is ready')
def step_impl(context):
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


@step(u'quit appium')
def quit_appium(context):
    if hasattr(context, 'appiumSession'):
        context.appiumSession.quit()
        pass


@step(u'Find "{Text}" on screen')
def find_text_on_screen(context, Text):
    return finger.f_FindTargetByXPath(
        context.appiumSession,
        "android.widget.TextView", "text", Text
    )


@step(u'Find "{sId}" on screen, timeout {sTimeout} seconds')
def find_recourceid_on_screen_with_timeout(context, sId, sTimeout):
    """
        loop until the element available on screen. return the elements found.
    """
    els = []
    for i in range(1, int(sTimeout) + 1):
        sleep(1)
        els = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )
        if len(els) > 0:
            break

    return els


@step(u'Wait "{sId}" on screen, timeout {sTimeout} seconds')
def wait_recourceid_on_screen_with_timeout(context, sId, sTimeout):
    """
        loop until the element not appears on screen, assume the element is already on screen.
    """
    els = []
    for i in range(1, int(sTimeout) + 1):
        sleep(1)
        els = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )
        if len(els) < 1:
            break

    return els


@step(u'Wait until screen ready, timeout {ready_timeout} seconds')
def step_impl(context, ready_timeout):
    """
        Wait until screen is ready for click
        current definition:
            - all loading bar gone, TBA
    """
    # Resource-id com.tinklabs.launcher:id/loading

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
    #     logging.debug('screen keeps busy in %s seconds' % ready_timeout)
    #     # assert False

    pass

# TODO: delete me
# @step(u'{sAction} "{sId}" on screen, timeout {sTimeout} seconds')
# def step_impl(context, sAction, sId, sTimeout):
#     """
#         to Find/Wait ResourceId on screen, given by timeout sTimeout

#         :Args:
#             - sAction - Find / Wait
#             - sId - resourceId
#             - sTimeout - Timeout of this operation
#     """
#     dParameter = {}
#     dParameter['sId'] = sId
#     dParameter['sTimeout'] = sTimeout
#     dParameter['sAction'] = sAction

#     if sAction in ['Find']:
#         context.execute_steps(u'''
#             Then Find "%(sId)s" on screen, timeout %(sTimeout)s seconds
#         ''' % dParameter)
#     elif sAction in ['Wait']:
#         context.execute_steps(u'''
#             Then Wait "%(sId)s"
#         ''')
#         if len(lLookFor)<1:
#             break
#     elif:
#         print('the sAction=%s have nothing match' % sAction)
#         assert False


@step(u'Fail if the "{Text}" not appears on screen')
def fail_if_the_text_not_appears(content, Text):
    lLookFor = find_text_on_screen(content, Text)
    if isinstance(lLookFor, list) and len(lLookFor) == 1:
        pass
    else:
        assert False

# @step(u'Fail if the button "{sText}" not appears')


@step(u'Fail if the button "{Text}" not appears on screen')
def step_impl(context, Text):
    """
        find the button/textview by the text given by Text
        assert fail if nothing found
    """
    lLookFor = finger.f_FindButtonWithText(
        context.appiumSession, Text
    )

    if isinstance(lLookFor, list) and len(lLookFor) == 1:
        pass
    else:
        print(lLookFor)
        assert False


@step(u'Fail if the Text "{sText}" {sDetermin} appears on screen')
def step_impl(context, sText, sDetermin):
    """
        find the textview by the text given by Text
        decision made by sDetermin
            1. sDetermin = is , the False assertion applied when text found on screen
            2. sDetermin = not, the False assertion applied when text not found on screen
    """
    context.execute_steps(u'''
        Then Wait until screen ready, timeout 60 seconds
    ''')

    lLookFor = finger.f_FindElementsWithText(
        context.appiumSession, sText
    )

    if isinstance(lLookFor, list) and len(lLookFor) > 0:
        # NOTE the text found which is unwanted
        if sDetermin in ['is']:
            assert False
    else:
        # NOTE the text not found which is wanted
        if sDetermin in ['not']:
            assert False


@step(u'Check if the {sText} appears on screen')
def step_impl(context, sText):
    return len(finger.f_FindElementsWithText(
        context.appiumSession, sText
    ))


@step(u'Fail if the resources-id"{sId}" not appears')
def step_impl(context, sId):
    """
        NOTE: debug function for llaw
    """
    lLookFor = finger.f_FindTargetById(
        context.appiumSession,
        sId
    )

    if isinstance(lLookFor, list) and len(lLookFor) == 1:
        pass
    else:
        assert False


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

    lLookFor = []

    start_time = get_epoch_time()
    end_time = start_time + int(sTimeout)

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


@step(u'Wait until Video"{sId}" appears, timeout {sTimeout} seconds')
def step_impl(context, sId, sTimeout):
    lLookFor = []

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
        assert False


@step(u'Fail if the Video"{sId}" not appears')
def step_impl(context, sId):
    lLookFor = finger.f_FindTargetById(
        context.appiumSession,
        sId
    )

    if isinstance(lLookFor, list) and len(lLookFor) > 0:
        pass
    else:
        assert False

# @step(u'Fail if the button "{sText}" not appears')
# def step_impl(context, sText):
#     lLookFor = finger.f_FindButtonWithText(sText)

#     if isinstance(lLookFor, list) and len(lLookFor) == 1:
#         pass
#     else:
#         assert False


@step(u'tap screen {n} times at {somewhere}')
def step_impl(context, n, somewhere):
    finger.f_TapScreen(context.appiumSession, 1, 1, 1)


@step(u'tap on Text "{sText}"')
def step_impl(context, sText):
    """
    wait until screen ready, tap on the element by its text

    Args:
        sText: the text wanted to tap

    """
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
        logging.error('cannot find the wanted text')
        assert False, 'cannot find the wanted text: %s' % sText
    pass


@step(u'press "{dPadKey}" button')
def step_impl(context, dPadKey):
    finger.f_PressKey(context.appiumSession, dPadKey)


@step(u'press {ButtonName} button')
def step_impl(context, ButtonName):
    if ButtonName == 'HOME':
        finger.f_PressKey(context.appiumSession, android_key_const.HOME)


@step(u'tap on button "{sWidget}":"{sProperties}":"{sDescription}"')
def step_impl(context, sWidget, sProperties, sDescription):
    context.execute_steps(u'''
        Given Wait until screen ready, timeout 60 seconds
    ''')
    finger.f_TapWidgetByPropertiesAndValue(
        context.appiumSession,
        sWidget, sProperties, sDescription)
    sleep(1)
    pass


@step(u'tap on checkbox "{sWidget}":"{sProperties}":"{sDescription}"')
def step_impl(context, sWidget, sProperties, sDescription):
    finger.f_TapWidgetByPropertiesAndValue(
        context.appiumSession,
        sWidget, sProperties, sDescription)
    sleep(1)
    pass


# and Fail if the activity "com.tinklabs.launcher.features.main.activity.LauncherActivity" not active in "10" seconds
@step(u'Fail if the activity "{sActivity}" not active in "{sSeconds}" seconds')
def step_impl(context, sActivity, sSeconds):
    """
        wrapper for appium wait_activity
    """
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


@step(u'tap on position "{sX}","{sY}" using adb')
def step_impl(context, sX, sY):
    """
        tap on specific position
        TODO: handle this using appium. unknown temporary solution
    """

    # sTapCmd = "adb shell input tap %s %s" % (sX, sY)
    # lCmd = sTapCmd.split(' ')
    # subprocess.check_output(lCmd)

    logging.debug('adb tap on screen position %s, %s' % (sX, sY))
    context.adb_session.run_cmd('shell input tap %s %s' % (sX, sY))

    pass


@then(u'Fail if the content-desc "{sText}" {sDetermine} appears on screen')
def step_impl(context, sText, sDetermine):
    els = finger.f_FindElementsWithContentDesc(context.appiumSession, sText)

    if els:
        # NOTE content-desc appears on screen
        if sDetermine in ['is']:
            assert False, 'the unwanted elements %s appears on screen' % sText
    else:
        if sDetermine in ['not']:
            assert False, 'the wanted elements %s not appears on screen' % sText
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
        logging.error('cannot find free port for appium')
        assert False, 'cannot find free port for appium'

    return result


@step(u'noop')
def step_impl(context):
    print('i am supposed no operation, just an print out only')


@given(u'a new working directory')
def step_impl(context):
    logging.info(u'STEP: Given a new working directory')


@given(u'a file named "{filename}" with')
def step_impl(context, filename):
    logging.debug(u'STEP: create file with content')

    f = open(filename, 'w')
    f.write(context.text)
    f.close()


@given(u'start appium')
def step_impl(context):
    """
    try to initiate the appium by behave.
    port number is picken by random
    udid (serial number on android) is by the context.android_serial
    """
    logging.debug(u'STEP: Given start appium')

    appium_port = get_free_port(range(4723, 4723 + 999))

    # NOTE: using 1 on 1 strategy, currently supposed the number of appium session is same as the number of device attached

    appium_command = PATH_APPIUM_BINARY + \
        ' -U %s --port %d' % (context.android_serial, appium_port)
    logging.debug('android_serial:%s' % context.android_serial)
    logging.debug('appium_port:%d' % appium_port)
    logging.debug("appium_command: %s" % appium_command)

    appium_process = subprocess.Popen(
        appium_command.split(' '), stdout=subprocess.PIPE
    )
    logging.debug(appium_command)

    # TODO: remove me
    # context.appiumSession = webdriver.Remote(
    #     'http://localhost:4723/wd/hub',
    #     desired_caps)
    context.appium_port.append(appium_port)
    context.appium_pid.append(appium_process.pid)

    # wait some seconds for appium start
    sleep(5)


@step(u'stop appium')
def step_impl(context):
    logging.debug(u'STEP: stop appium')

    # TODO: move me up
    import psutil

    for pid in context.appium_pid:
        os.kill(pid, signal.SIGTERM)


@given(u'setup android appium demo app')
def step_impl(context):
    logging.debug(u'STEP: Given setup android appium demo app')

    desired_caps = {}
    desired_caps['platformName'] = 'android'
    # desired_caps['platformVersion'] = '7.0'
    desired_caps['deviceName'] = 'VZHGLMA742804186'
    desired_caps['app'] = PATH(
        '/Users/louis_law/.android_tinklabs/ApiDemos-debug.apk'
    )

    context.appium_session = webdriver.Remote(
        'http://localhost:%s/wd/hub' % context.appium_port[0], desired_caps)


# @step(u'Wait until screen load complete, timeout {sSeconds} seconds')
# def step_impl(context, sSeconds):
#     """
#         blocker until page load/render complete
#         current page load indicator
#             - resource-id - com.tinklabs.launcher:id/loading
#             - className - android.widget.ProgressBar
#     """
#     print('i am supposed to wait until page load complete, timeout %s seconds' % sSeconds)

#     context.execute_steps(u'''
#         Then
#     ''')
