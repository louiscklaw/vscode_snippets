
from behave import given, when, then, step
import os
import sys
import subprocess

from collections import deque

from time import sleep

# https://github.com/appium/python-client
from appium import webdriver

# android stuff
import android_capabilities

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

from android_const import android_key_const
from android_const import android_os_permission_button


from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction





DUT_DEVICE = 'VZHGLMA750300169'



def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# com.tinklabs.activateapp_base.apk
# @step('the activateapp is running on "{platform}" "{type}" ver "{version}"')
# def


# com.example.android.apis
# Given started package "<Package>" activity "<Activity>" on "<platform>" type "<type>" ver "<version>"#


# com.example.android.apis
# Given started package "<Package>" activity "<Activity>" on "<platform>" type "<type>" ver "<version>"#

@step('Target device is {device}')
def step_impl(context, device):
    context.device = device

@step('{process_wanted} is running')
def step_impl(context, process_wanted):
    try:
        if os.popen( "ps -ef | grep -i %s | grep -v 'grep'" % process_wanted ).read().strip().find(process_wanted) > -1:
            pass
        else:
            assert False
    except Exception, e:
        raise e
        assert False



@step('setup an android as below')
def step_impl(context):
    row = context.table[0]

    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    # desired_caps['platformVersion'] = row['version']
    desired_caps['deviceName'] = 'Android'
    # desired_caps['app'] = row['PATH(packageName)']
    desired_caps['appPackage'] = row['Package']
    desired_caps['appActivity'] = row['Activity']
    desired_caps['deviceReadyTimeout'] = 30
    desired_caps['noReset'] = False

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


# debug
# sleep 1 seconds
# sleep 5 seconds
# sleep 15 seconds
# sleep 30 seconds
# sleep 60 seconds
@step('sleep {n} seconds')
def step_impl(context, n):
    """
        sleep for n seconds
        :input: n -> integer
        output: none
    """
    sleep(int(n))

@step('halt myself')
def step_impl(context):
    """
        sleep long enough for troubleshoot purpose
    """
    sleep(99999)



# com.tinklabs.launcher.apk
@step(u'User tap on "{button}" button')
def step_impl(context, button):
    finger.f_FindButtonWithText(context.appiumSession, button)[0].click()


# @then(u'Fail if "{component}", "{activity}" not active')
# def step_impl(context, component, activity):
#     """check the active android activity on screen"""
#     if component + '/' + activity != finger.f_CheckCurrentActivity(context.appiumSession):
#         assert False

@step('Test setup is ready')
def step_impl(context):
    context.execute_steps(u'''
      Given appium is running

      Given FASTBOOT Erase userdata
        And ADB Wait for device, timeout 600 seconds
        And ADB check boot completed, timeout 1200 seconds

      Then Wait for handy initialization
        And ADB Initialize android
    ''')

@step('quit appium')
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
    for i in range(1,int(sTimeout)+1):
        sleep(1)
        els = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )
        if len(els) > 0 :
            break

    return els

@step(u'Wait "{sId}" on screen, timeout {sTimeout} seconds')
def wait_recourceid_on_screen_with_timeout(context, sId, sTimeout):
    """
        loop until the element not appears on screen, assume the element is already on screen.
    """
    els = []
    for i in range(1,int(sTimeout)+1):
        sleep(1)
        els = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )
        if len(els) < 1 :
            break

    return els


@step(u'Wait until screen ready, timeout {sTimeout} seconds')
def step_impl(context, sTimeout):
    """
        Wait until screen is ready for click
        current definition:
            - all loading bar gone, TBA
    """
    # Resource-id com.tinklabs.launcher:id/loading

    iTimeout = int(sTimeout)
    dqiElementFound = deque([1,1,1])

    for i in range(1, iTimeout):
        sleep(1)
        dqiElementFound.popleft()
        dqiElementFound.append(len(wait_recourceid_on_screen_with_timeout(context, "com.tinklabs.launcher:id/loading", '1')))

        if not(any(dqiElementFound)):
            break


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
#         context.execute_step(u'''
#             Then Find "%(sId)s" on screen, timeout %(sTimeout)s seconds
#         ''' % dParameter)
#     elif sAction in ['Wait']:
#         context.execute_step(u'''
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

# @step('Fail if the button "{sText}" not appears')
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

@step('Fail if the resources-id"{sId}" not appears')
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

@step('Wait until "resource-id" "{sId}" appears on screen, timeout {sTimeout} seconds')
def step_impl(context, sId, sTimeout):
    """
        Try to locate sId on current screen, timeout given by sTimeout

        :Args:
            - sId - recource-id
            - sTimeout - timeout second
    """

    lLookFor = []

    for i in range(1,int(sTimeout)+1):
        sleep(1)
        lLookFor = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )

        if len(lLookFor)>0:
            break

    if len(lLookFor) > 0:
        pass
    else:
        assert False
    pass

@step('Wait until Video"{sId}" appears, timeout {sTimeout} seconds')
def step_impl(context, sId, sTimeout):
    lLookFor = []

    for i in range(1,int(sTimeout)+1):
        sleep(1)
        lLookFor = finger.f_FindTargetById(
            context.appiumSession,
            sId
        )

        if len(lLookFor)>0:
            break

    if len(lLookFor) > 0:
        pass
    else:
        assert False

@step('Fail if the Video"{sId}" not appears')
def step_impl(context, sId):
    lLookFor = finger.f_FindTargetById(
        context.appiumSession,
        sId
    )

    if isinstance(lLookFor, list) and len(lLookFor) > 0:
        pass
    else:
        assert False

# @step('Fail if the button "{sText}" not appears')
# def step_impl(context, sText):
#     lLookFor = finger.f_FindButtonWithText(sText)

#     if isinstance(lLookFor, list) and len(lLookFor) == 1:
#         pass
#     else:
#         assert False

@step('tap screen {n} times at {somewhere}')
def step_impl(context, n, somewhere):
    finger.f_TapScreen(context.appiumSession, 1, 1, 1)

@step('tap on Text "{sText}"')
def step_impl(context, sText):
    # finger.f_TapWidgetByPropertiesAndValue(
    #     context.appiumSession,
    #     "android.widget.TextView",
    #     "text", sText)
    # sleep(3)
    # pass
    els = finger.f_FindElementsWithText(
        context.appiumSession, sText
    )
    if els:
        sleep(1)
        els[0].click()

        # NOTE for debug
    else:
        assert False
    pass



@step(u'press "{dPadKey}" button')
def step_impl(context, dPadKey):
    finger.f_PressKey(context.appiumSession, dPadKey)


@step(u'press {ButtonName} button')
def step_impl(context, ButtonName):
    if ButtonName == 'HOME':
        finger.f_PressKey(context.appiumSession, android_key_const.HOME)


@step('tap on button "{sWidget}":"{sProperties}":"{sDescription}"')
def step_impl(context, sWidget, sProperties, sDescription):
    finger.f_TapWidgetByPropertiesAndValue(
        context.appiumSession,
        sWidget, sProperties, sDescription)
    sleep(1)
    pass


@step('tap on checkbox "{sWidget}":"{sProperties}":"{sDescription}"')
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

    if bResult :
        pass
    else:
        print('cannot find activity %s' % sActivity)
        assert False

@step('tap on position "{sX}","{sY}" using adb')
def step_impl(context, sX, sY):
    """
        tap on specific position
        TODO handle this using appium. unknown temporary solution
    """
    sTapCmd = "adb shell input tap %s %s" % (sX, sY)
    lCmd = sTapCmd.split(' ')
    subprocess.check_output(lCmd)
    sleep(1)

    pass



@then(u'Fail if the content-desc "{sText}" {sDetermine} appears on screen')
def step_impl(context, sText, sDetermine):
    els = finger.f_FindElementsWithContentDesc(context.appiumSession,sText)

    if els:
        # NOTE content-desc appears on screen
        if sDetermine in ['is']:
            assert False
    else:
        if sDetermine in ['not']:
            assert False
    pass



@step(u'noop')
def step_impl(context):
    print('i am supposed no operation, just an print out only')


# @step(u'Wait until screen load complete, timeout {sSeconds} seconds')
# def step_impl(context, sSeconds):
#     """
#         blocker until page load/render complete
#         current page load indicator
#             - resource-id - com.tinklabs.launcher:id/loading
#             - className - android.widget.ProgressBar
#     """
#     print('i am supposed to wait until page load complete, timeout %s seconds' % sSeconds)

#     context.execute_step(u'''
#         Then
#     ''')
