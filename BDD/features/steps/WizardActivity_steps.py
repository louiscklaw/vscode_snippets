#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
sys.path.append(os.path.dirname(__file__) + '/../_lib')

from behave import given, when, then, step

from config import *

from time import sleep
from android_function import finger

# behave specific import
from WizardActivity_config import *
from WizardActivityPage import *

from devices import *


@given(u'Wait for "{Text}" ("{n}" countdown)')
def step_impl(context, Text, n):
    """to handle 'waiting for network connection...'"""
    iCountDown = int(n)
    bTextNotFound = True

    while iCountDown > 0 and bTextNotFound:
        iCountDown -= 1
        sleep(1)
        if None != finger.f_FindTargetByXPath(
            context.appiumSession,
            "android.widget.TextView", "text", Text
        ):
            bTextNotFound = False
    pass


@given(u'Reach "Become a handy member" page')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Given Reach "Become a handy member" page')


@given(u'Reach "Log in to yo your handy account" page')
def step_impl(context):
    raise NotImplementedError(
        u'STEP: Given Reach "Log in to yo your handy account" page')


@step(u'Reach "{target}" page in WizardActivity by skip, route "{route}"')
def step_impl(context, target, route):
    """
        a new WizardActivity to handle with different route
        currently only target "Happy flow The end available

        :Args:
            - target, target stage in Wizard tour
            - route, not effective, reserved
                route of Wizard, currently mapped with hotel of the device, e.g. QA Testing(IRX)
    """
    lsTemp = []

    if context.device == 'T1':
        # 1280 x 700

        # IDEA: i think i need a route class here
        # happy flow means skip to the end
        config_T1 = WizardActivityPageConfig('T1')
        WizardActivityPage_T1 = WizardActivityPageGenerator(config_T1)

        if target == 'Happy flow The end':
            lsTemp.append(WizardActivityPage_T1.get_page(INIT))
            lsTemp.append(WizardActivityPage_T1.get_page(WV_GREETING))
            lsTemp.append(
                WizardActivityPage_T1.get_page(WV_SKIP_CHECKOUT_DATE))
            lsTemp.append(
                WizardActivityPage_T1.get_page(WV_SKIP_HANDYMEMBER))
            # lsTemp.append(
            #     WizardActivityPage_T1.get_page(WV_SKIP_PERSONALIZED_EXPERIENCE))
            lsTemp.append(
                WizardActivityPage_T1.get_page(WV_PASS_PLAY_VIDEO))

    elif context.device == 'M812':
        # screen resolution is 1920 x 1080
        # temporary for M812
        # landing on checkout date page
        if target == 'Happy flow The end':
            # updating for QA Testing(IRX)
            lsTemp.append(WizardActivityPage.dWizardActivityPage[INIT])
            lsTemp.append(WizardActivityPage.dWizardActivityPage[WV_GREETING])
            # lsTemp.append(WizardActivityPage.dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])
            lsTemp.append(
                WizardActivityPage.dWizardActivityPage[WV_SKIP_HANDYMEMBER])
            # lsTemp.append(WizardActivityPage.dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE])
            lsTemp.append(
                WizardActivityPage.dWizardActivityPage[WV_PASS_TUTORIAL_IMAGE])
        else:
            logging.error('target: %s is not handled' % target)
            assert False

    context.execute_steps(''.join(lsTemp))

    pass


@step(u'Reach "{target}" page in WizardActivity by skip')
def step_impl(context, target):
    """
        NOTE: to be obsoleted
        a procedure to handle the state of activation wizard
        NOTE: current route = QA12 , panda hotel
            - finguring how to define route, currently map it with hotel 1st.
    """

    INIT = 0
    WV_GREETING = 1
    WV_SKIP_CHECKOUT_DATE = 2
    WV_SKIP_HANDYMEMBER = 3
    WV_SKIP_PERSONALIZED_EXPERIENCE = 4
    WV_PASS_PLAY_VIDEO = 5

    dWizardActivityPage = {}
    dWizardActivityPage[INIT] = u'''
        Then tap on position "0","0" using adb
          And sleep 3 seconds
          And Fail if the Text "English" not appears on screen
    '''

    dWizardActivityPage[WV_GREETING] = u'''
        # check the box next to Terms and Conds
        Then tap on position "60","1242" using adb
          And sleep 5 seconds
          And tap on button "android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"
          And sleep 3 seconds
    '''

    dWizardActivityPage[WV_SKIP_CHECKOUT_DATE] = u'''
        # bypass checkout day currently, i should press the skip button
        Then Wait until "When are you checking out?" appears on screen, timeout "10" seconds
        #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
        #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
          And tap on text "SKIP"
    '''

    dWizardActivityPage[WV_SKIP_HANDYMEMBER] = u'''
        # Then bypass facebook registration currently, i should press the skip button
        Then Wait until Text startwith "Become a handy member!" appears on screen, timeout "10" seconds
        Then sleep 1 seconds
        #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
        #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
          And tap on text "I'll do it later"
    '''

    dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE] = u'''
        # Then bypass personalize experience registration currently, i should press the skip button
        # Then sleep 1 seconds
        Then Wait until Text startwith "Let us personalize" appears on screen, timeout "10" seconds
          And sleep 1 seconds
        #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
        #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
          And tap on text "SKIP"
    '''

    dWizardActivityPage[WV_PASS_PLAY_VIDEO] = u'''
        # # wait a moment for video to load
        # Then Wait until Video"com.tinklabs.launcher:id/video_view" appears, timeout 60 seconds
        #   And Fail if the Video"com.tinklabs.launcher:id/video_view" not appears

        # Let's start should appears
        Then Wait until "Let's Start" appears on screen, timeout "120" seconds
          And Fail if the button "Let's Start" not appears on screen
          And tap on text "Let's Start"
    '''

    lsTemp = []
    # landing on checkout date page
    if target == 'ask for checkout date':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
    # landing on "Become a handy member" page
    elif target == 'Become a handy member':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])

    elif target == 'Personalized experience':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])
        lsTemp.append(dWizardActivityPage[WV_SKIP_HANDYMEMBER])

    elif target == 'Play video':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])
        lsTemp.append(dWizardActivityPage[WV_SKIP_HANDYMEMBER])
        lsTemp.append(dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE])

    elif target == 'Happy flow The end':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])
        lsTemp.append(dWizardActivityPage[WV_SKIP_HANDYMEMBER])
        lsTemp.append(dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE])
        lsTemp.append(dWizardActivityPage[WV_PASS_PLAY_VIDEO])

    context.execute_steps(''.join(lsTemp))

    pass


@step(u'Wait until "{Text}" {appears} on screen, timeout "{TimeOut}" seconds')
def step_impl(context, Text, TimeOut, appears):
    """
    Just wait the target Text appears, counted down by TimeOut seconds
    """

    # TODO: temporary solution

    # NOTE: defaults to T1 device
    (dummy_tap_x, dummy_tap_y) = Device_T1.DUMMY_TAP

    if context.device == 'M812':
        (dummy_tap_x, dummy_tap_y) = Device_M812.DUMMY_TAP

    TextFound = False
    TimeOut = int(TimeOut)
    for i in range(1, TimeOut):
        sleep(1)
        logging.debug('wait and retry')
        context.execute_steps(u'''
            Given Wait until screen ready, timeout 1 seconds
            Then tap on position "%d","%d" using adb
        ''' % (dummy_tap_x, dummy_tap_y)
        )

        els = finger.f_FindElementsWithText(context.appiumSession, Text)
        if appears in ['appears']:
            # NOTE i want it on screen
            if len(els) > 0:
                TextFound = True
                break
        elif appears in ['not appears']:
            # NOTE i don't want it on screen
            if len(els) < 1:
                break

    if not(TextFound):
        if appears in ['appears']:
            assert False

    pass


@step(u'Wait until Text startwith "{Text}" appears on screen, timeout "{TimeOut}" seconds')
def step_impl(context, Text, TimeOut):
    """
    Just wait the target Text appears, counted down by TimeOut seconds
    """
    # print('i am supposed a waiting until %s' % Text)

    TextFound = False
    TimeOut = int(TimeOut)
    for i in range(1, TimeOut):
        sleep(1)
        context.execute_steps(u'''
            Then tap on position "0","1201" using adb
        ''')
        els = finger.f_FindElementsStartWithText(context.appiumSession, Text)
        if len(els) > 0:
            TextFound = True
            break

    if not(TextFound):
        assert False, '%s not found' % Text

    pass


@step(u'erase from unknown stage')
def step_impl(context):
    """
    Stored procedure to align the device from unknown stage, e.g. device hang in the middle of the test.
    based on the value of device in context
    """
    if context.device == 'M812':
        context.execute_steps(u'''
            Given fastboot erase M812
                And ADB Wait for device, timeout 60 seconds
                And ADB check boot completed, timeout 600 seconds
            Then Wait for handy initialization
                And ADB Initialize android
        ''')
