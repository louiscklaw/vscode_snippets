from behave import given, when, then, step
import os
import sys

# https://github.com/appium/python-client
from appium import webdriver
import android_capabilities

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


@step(u'Clear all handy settings')
def step_impl(context):
    """
        clear tinklabs related settings
        to make a lighter erase environment rather that FASTBOOT erase
    """
    context.execute_steps(u'''
        Given sleep 1 seconds
          And adb shell "pm clear com.tinklabs.activateapp"
          And adb shell "pm clear com.tinklabs.handyappinstaller"
          And adb shell "pm clear com.tinklabs.handybeacon"
          And adb shell "pm clear com.tinklabs.handychat"
          And adb shell "pm clear com.tinklabs.handyclock"
          And adb shell "pm clear com.tinklabs.handydeals"
          And adb shell "pm clear com.tinklabs.handyphone"
          And adb shell "pm clear com.tinklabs.handyremotedebug"
          And adb shell "pm clear com.tinklabs.handyxposed"
          And adb shell "pm clear com.tinklabs.launcher"
          And adb shell "pm clear com.tinklabs.otaupdate"
          And adb shell "pm clear com.tinklabs.softsim"
          And adb shell "pm clear com.tinklabs.wifiscanner"
    ''')

@step(u'Wait for handy initialization')
def step_impl(context):
    """
        sleep across the handy initialization
    """
    context.execute_steps(u'''
        Then
    ''')
