from behave import given, when, then, step
import os
import sys

from time import sleep

# https://github.com/appium/python-client
from appium import webdriver
import android_capabilities

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# com.tinklabs.launcher.apk
@step(u'tap on highlight deal {sPosition} in Tickets')
def step_impl(context, sPosition):
    """
        To handle the highlight deal in Ticket first page

        :Args:
            sPosition - the position of the highlighted deal
                expected to be 1 / 2 / 3
    """
    els = finger.f_FindElementsById(context.appiumSession, "com.tinklabs.handydeals:id/image")

    # Expected: Fail if no highlght deals found
    assert len(els) > 0

    els[0].click()

# @then(u'Fail if "{component}", "{activity}" not active')
# def step_impl(context, component, activity):
#     """check the active android activity on screen"""
#     if component + '/' + activity != finger.f_CheckCurrentActivity(context.appiumSession):
#         assert False

@step(u'tap on back arrow in highlight deals detail page')
def step_impl(context):
    """
        To handle the back arrow in highlight deals detail page (top left corner in T1)
        TODO: for llaw reference, the button didn't got a friendly accessable-id with it. hard to address the button
    """

    sToolbar   = 'new UiSelector().resourceId("com.tinklabs.handydeals:id/toolbar")'
    sBackArrow = 'new UiSelector().className("android.widget.ImageButton")'

    sUiQuery   = '%s.childSelector(%s)' % (sToolbar, sBackArrow)

    els = finger.f_FindElementsByUiAutomator(context.appiumSession, sUiQuery)

    # Expected a element to be found
    assert len(els) > 0

    els[0].click()
