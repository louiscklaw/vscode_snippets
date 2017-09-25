#!WizardActivity_steps.py
from behave import given, when, then, step
import os
import sys

from time import sleep

sys.path.append(os.path.dirname(__file__) + '/../_lib')
from android_function import finger


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
    raise NotImplementedError(u'STEP: Given Reach "Become a handy member" page')

@given(u'Reach "Log in to yo your handy account" page')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Reach "Log in to yo your handy account" page')

@step(u'Reach "{Target}" page in WizardActivity by skip')
def step_impl(context, Target):
    """
        a procedure to handle the state of activation wizard
    """
    INIT=0
    WV_GREETING=1
    WV_SKIP_CHECKOUT_DATE=2
    WV_SKIP_HANDYMEMBER=3
    WV_SKIP_PERSONALIZED_EXPERIENCE=4
    WV_PASS_PLAY_VIDEO=5

    dWizardActivityPage={}
    dWizardActivityPage[INIT]=u'''
        Then tap on position "0","0" using adb
          And sleep 3 seconds
          And Fail if the Text "English" not appears on screen
    '''

    dWizardActivityPage[WV_GREETING]=u'''
        # check the box next to Terms and Conds
        Then tap on position "60","1242" using adb
          And sleep 5 seconds
          And tap on button "android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"
          And sleep 3 seconds
    '''

    dWizardActivityPage[WV_SKIP_CHECKOUT_DATE]=u'''
        # bypass checkout day currently, i should press the skip button
        Then Wait until "When are you checking out?" appears on screen, timeout "10" seconds
          And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
          And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
    '''

    dWizardActivityPage[WV_SKIP_HANDYMEMBER] =u'''
        # Then bypass facebook registration currently, i should press the skip button
        Then sleep 1 seconds
          And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
          And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
    '''

    dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE]=u'''
        # Then bypass personalize experience registration currently, i should press the skip button
        Then sleep 1 seconds
          And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
          And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"

        # # Optional dialogue appears on linux
        # Then Wait until "Use USB to transfer files?" appears on screen, timeout "60" seconds
        #   And tap on text "CANCEL"

    '''

    dWizardActivityPage[WV_PASS_PLAY_VIDEO]=u'''
        # wait a moment for video to load
        Then Wait until Video"com.tinklabs.launcher:id/video_view" appears, timeout 60 seconds
          And Fail if the Video"com.tinklabs.launcher:id/video_view" not appears

        # Let's start should appears
        Then Wait until "Let's Start" appears on screen, timeout "180" seconds
          And Fail if the button "Let's Start" not appears on screen
          And tap on text "Let's Start"
    '''

    lsTemp=[]
    # landing on checkout date page
    if Target == 'ask for checkout date':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
    # landing on "Become a handy member" page
    elif Target == 'Become a handy member':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])

    elif Target == 'Personalized experience':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])
        lsTemp.append(dWizardActivityPage[WV_SKIP_HANDYMEMBER])

    elif Target == 'Play video':
        lsTemp.append(dWizardActivityPage[INIT])
        lsTemp.append(dWizardActivityPage[WV_GREETING])
        lsTemp.append(dWizardActivityPage[WV_SKIP_CHECKOUT_DATE])
        lsTemp.append(dWizardActivityPage[WV_SKIP_HANDYMEMBER])
        lsTemp.append(dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE])

    elif Target == 'Happy flow The end':
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
    # print('i am supposed a waiting until %s' % Text)

    TextFound = False
    TimeOut = int(TimeOut)
    for i in range(1, TimeOut):
        sleep(1)
        context.execute_steps(u'''
          Then tap on position "0","1201" using adb
        ''')
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
        assert False

    pass
