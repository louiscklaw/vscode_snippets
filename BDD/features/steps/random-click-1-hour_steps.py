#! random-click-1-hour_steps.py
from behave import given, when, then, step
import os
import sys

import logging
logging.basicConfig(level=logging.INFO)

from behave import given, when, then, step
import time
import random

from android_function import finger

from random import randint

sys.path.append(os.path.dirname(__file__) + '/../_lib')

lsRandomTour = []
# lsRandomTour.append(u'Then Swipe the feed until %s appears' % 'Survey')
# lsRandomTour.append(u'Then Swipe the feed until %s appears' % 'DISCOUNT TICKETS')
# lsRandomTour.append(u'Then Swipe the feed until %s appears' % 'TRENDING')
# lsRandomTour.append(u'Then Swipe the feed until %s appears' % 'FUN FACTS')
# lsRandomTour.append(u'Then Try to activate handy phone from launcher')

# TODO: need troubleshoot
lsRandomTour.append(u'Then Activate App Drawer from launcher')
lsRandomTour.append(u'Then Swipe up in App Drawer until "Erase Data" appears')
lsRandomTour.append(u'Then Click on a random clickable (depth:4)')


@step(u'Random tour selftest, route{route_number}')
def step_impl(context, route_number):
    """
    self test for random tour, run a predefined tour

    Args:
        route_number: the index of the tour
    """

    # NOTE: self test
    context.execute_steps(lsRandomTour[int(route_number)])


@step(u'Random tour for {sDuration} hour')
def step_impl(context, sDuration):
    """
        Perform click by random manner for a duration

        :Args:
            - duration - the duration how long the click (repetive, constitutive) should be made
                - exepcted an integer
        :NOTE:
            - corelated the mixpanel
    """
    iRoute = 0
    try:
        fDuration = float(sDuration)
        fDurationInSecond = fDuration * 3600
        iTimeToStop = time.time() + fDurationInSecond

        print(u'I am supposed to click on clickable for %f seconds' %
            fDurationInSecond)

        iRunCount = 0
        while time.time() < iTimeToStop:
            # for iRoute in range(0,len(lsRandomTour)):
            iRunCount += 1
            iRoute = random.randint(0, len(lsRandomTour) - 1)

            print('continue to random click, run count %d' % iRunCount)
            context.execute_steps(
                lsRandomTour[iRoute]
            )

        pass
    except Exception as e:
        print('iRoute:%d' % iRoute)
        raise e
    else:
        pass


# HOME
@step(u'Swipe the feed until {sText} appears')
def step_impl(context, sText):
    """
    Just an random click route 1, reference by mixpanel

    Args:
        sText: the text expected, represent the text in the feed.
     """
    dParameter = {}
    dParameter['sText'] = sText

    context.execute_steps(u'''
        # NOTE to check if the browser shown up
        Then press HOME button
          And ADB screen capture, save to "./_screenshot"
        # And Fail if the Text "Home" not appears on screen

        Then Swipe "com.tinklabs.launcher:id/mdContent" UP Distance "400" until text containing "%(sText)s" appears on screen (max swipe "900")
          And ADB screen capture, save to "./_screenshot"

        # Check after work
        # Temporary workaround for the swipe down
        #   And Fail if the Text "%(sText)s" not appears on screen

        Then Swipe "com.tinklabs.launcher:id/mdContent" DOWN Distance "200" until "Home" appears on screen (max swipe "10")
          And ADB screen capture, save to "./_screenshot"
        # And Fail if the Text "Home" not appears on screen
    ''' % dParameter)

# App drawer


@step(u'Activate App Drawer from launcher')
def step_impl(context):
    """
        Try to bring up App Drawer page
    """
    logging.debug('i am supposed to bring up the app drawer')

    context.execute_steps(u'''
        # To make sure Apps button appears
        Given press HOME button
          And Wait until screen ready, timeout 30 seconds
          And Swipe "com.tinklabs.launcher:id/mdContent" DOWN Distance "200" until "Apps" appears on screen (max swipe "5")

        Given User tap on "Apps" button
          And Wait until screen ready, timeout 30 seconds
          And Wait until "Google" appears on screen, timeout "30" seconds

        Then press HOME button
          And Wait until screen ready, timeout 30 seconds
          And Wait until "Home" appears on screen, timeout "30" seconds
    ''')


@step(u'Swipe up in App Drawer until "{sAppWantedOnScreen}" appears')
def step_impl(context, sAppWantedOnScreen):
    """
    Tap the App drawer and swipe until the sAppWantedOnScreen appears on screen

    Args:
        sAppWantedOnScreen: The wanted application.
    """

    logging.debug('i am supposed to do some swipe in App Drawer')

    context.execute_steps(u'''
        Given User tap on "Apps" button
            And Wait until screen ready, timeout 30 seconds

        Then Swipe "com.tinklabs.launcher:id/main_app_list" UP Distance "100" until "%s" appears on screen (max swipe "20")

        Then press HOME button
          And Wait until screen ready, timeout 30 seconds

          And Swipe "com.tinklabs.launcher:id/mdContent" DOWN Distance "200" until "Apps" appears on screen (max swipe "5")
          And Wait until screen ready, timeout 10 seconds

          And Wait until "Home" appears on screen, timeout "30" seconds
    ''' % sAppWantedOnScreen)


@step(u'Click on a random clickable')
def step_impl(context):
    """
        Try to click on an random link
    """

    # NOTE confirm screen ready before work
    context.execute_steps(u'''
        Then Wait until screen ready, timeout 30 seconds
    ''')

    els = finger.f_FindElementsClickable(context.appiumSession)
    els[randint(0, len(els) - 1)].click()

    # NOTE try to hold until page load complete
    context.execute_steps(u'''
        Then Wait until screen ready, timeout 10 seconds
    ''')

    pass


@step(u'Click on a random clickable (depth:{sDepth})')
def step_impl(context, sDepth):
    """
        make use of random clickable, and sleep for n seconds
    """

    for i in range(1, int(sDepth)):
        context.execute_steps(u'''
            Then ADB screen capture, save to "./_screenshot"
            Then Click on a random clickable
              And Wait until screen ready, timeout 30 seconds
            Then ADB screen capture, save to "./_screenshot"
        ''')

    context.execute_steps(u'''
        Then Click on a random clickable
          And Wait until screen ready, timeout 30 seconds
        Then ADB screen capture, save to "./_screenshot"

        Then press HOME button
          And Wait until screen ready, timeout 30 seconds
        Then ADB screen capture, save to "./_screenshot"
    ''')
