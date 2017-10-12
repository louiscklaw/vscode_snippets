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

# (sApkName, sHKOAppId) = ('../_apk/com.tinklabs.activateapp_base.apk', 'com.tinklabs.activateapp.features.wizard.WizardActivity')

# def before_all(context):
#     context.config.setup_logging()


# def after_scenario(context):
#     context.appiumSession.quit()

# https://pythonhosted.org/behave/tutorial.html
# Debug-on-Error (in Case of Step Failures)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR         (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=yes     (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=no      (to disable debug-on-error)
BEHAVE_DEBUG_ON_ERROR = os.getenv("BEHAVE_DEBUG_ON_ERROR", False)


def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def quit_appiumSession(context):
    context.appiumSession.quit()
    pass


def before_all(context):
    setup_debug_on_error(context.config.userdata)
    context.logger = setup_logger('handy_behave_run_logger')
    context.adb_binary = PATH_ADB_BINARY

    # behave initialization
    context.appium_port = []
    context.appium_pid = []


def after_all(context):
    pass


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)

    # louis.law add capability to capture screen if possible
    # if hasattr(context,'appiumSession'):
    #     context.execute_steps(u'''
    #         Then ADB screen capture, save to "/Users/louis_law/_temp"
    #     ''')


def before_step(context, scenario):
    pass


def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def uninstall_app(context, app_id):
    context.appiumSession.remove_app(app_id)
    pass


def quit_appiumSession(context):
    try:
        context.appiumSession.quit()
    except Exception as e:
        pass

    pass


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    pass


def after_scenario(context, scenario):
    if hasattr(context, 'appiumSession'):
        # uninstall_app(context, sHKOAppId)
        quit_appiumSession(context)
        print('quit appium session')
    pass


def before_tag(context, tag):
    pass


def after_tag(context, tag):
    pass


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    pass
