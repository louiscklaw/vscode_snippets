#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

from WizardActivityPage import *
# from WizardActivityPage import WizardActivityPageConfig
# from WizardActivityPage import WizardActivityPageGenerator

for device in ['T1', 'M812']:
    config_device = WizardActivityPageConfig(device)

    WizardActivityPage_device = WizardActivityPageGenerator(config_device)

    # NOTE: test generating page
    print WizardActivityPage_device.get_page(INIT)
    print WizardActivityPage_device.get_page(WV_GREETING)
    print WizardActivityPage_device.get_page(WV_SKIP_CHECKOUT_DATE)
    print WizardActivityPage_device.get_page(WV_SKIP_HANDYMEMBER)
    print WizardActivityPage_device.get_page(WV_SKIP_PERSONALIZED_EXPERIENCE)
    print WizardActivityPage_device.get_page(WV_PASS_PLAY_VIDEO)
    print WizardActivityPage_device.get_page(WV_PASS_TUTORIAL_IMAGE)


print
