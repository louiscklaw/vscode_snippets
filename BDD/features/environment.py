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
        context.execute_steps(u'''
            Then appium capture failed screen
        ''')
    pass

def before_step(context, scenario):
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
