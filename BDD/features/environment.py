# -- FILE:features/environment.py
from appium import webdriver
from time import sleep

import os
import sys
import subprocess

# NOTE: add custom library path
pLib = os.path.dirname(__file__) + '/_lib'
sys.path.append(pLib)

from android_function import finger
from android_function import util
from handy_logger import *

from config import *

import logging

import appium_function


def appium_capture_failed_screen(context):
    try:
        # TODO: remporary hardcode for the model
        print('capture failure screen invoked')
        print('saving to directory: %s' %
            context.device_config.PATH_FAILURE_SCREEN_CAPTURE)
        screen_capture = appium_function.appium_screen_capture(
            context.appiumSession, context.device_config.PATH_FAILURE_SCREEN_CAPTURE
        )
        screen_capture.capture_failed_screen()


    except Exception as e:
        print('error during capture the screen')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: context.device_config.PATH_FAILURE_SCREEN_CAPTURE')
        pprint(context.device_config.PATH_FAILURE_SCREEN_CAPTURE)

        raise e
    else:
        pass


def quit_appiumSession(context):
    context.appiumSession.quit()
    pass


def before_all(context):
    context.adb_binary = PATH_ADB_BINARY

    # behave initialization
    context.appium_port = []
    context.appium_pid = []


def after_all(context):
    pass


def after_step(context, step):
    if step.status == "failed":
        appium_capture_failed_screen(context)

    pass

def before_step(context, scenario):
    context.capture_screen_retry = 5
    pass


def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def uninstall_app(context, app_id):
    try:
        context.appiumSession.remove_app(app_id)
        pass
    except Exception as e:
        print('error during uninstall app')
        raise e
    else:
        pass
    pass


def quit_appiumSession(context):
    try:
        context.appiumSession.quit()
        print('exit appium session done')
    except Exception as e:
        print('error during quitting appium Session')
        pass

    pass


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    try:
        if hasattr(context, 'appiumSession'):
            # uninstall_app(context, sHKOAppId)
            quit_appiumSession(context)
            print('quit appium session')
        pass
    except Exception as e:
        print('error during quitting appium session')
        raise e
    else:
        pass

    pass


def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    pass
