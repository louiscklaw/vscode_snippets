from behave import given, when, then, step
import os
import sys

# https://github.com/appium/python-client
from appium import webdriver
import android_capabilities

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

@step(u'Try to activate handy phone from launcher')
def step_impl(context):
    """
        simple route to simulate user want to launch handy phone
    """
    context.execute_steps(u'''
        Given press HOME button
          And Wait until screen ready, timeout 30 seconds
          And Swipe "com.tinklabs.launcher:id/mdContent" DOWN Distance "200" until "Call" appears on screen (max swipe "5")

        Given User tap on "Call" button
          And Wait until "handy phone" appears on screen, timeout "30" seconds
    ''')
