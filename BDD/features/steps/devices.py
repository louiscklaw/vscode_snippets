#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint


class BasicDeviceConfig():
    # default configuration, based on T1
    DUMMY_TAP = (0, 1201)

    # for the very beginning checkbox
    GREETING_TAC_CHECKBOX = (60, 1242)
    pass


class Device_T1(BasicDeviceConfig):
    # NOTE: places for tapping to keep/refresh the screens
    GREETING_TAC_CHECKBOX = (60, 1242)

    DUMMY_TAP = (0, 1201)

    pass


class Device_M812(BasicDeviceConfig):
    # NOTE: for the checkbox at the bottom right corner of welcome screen
    GREETING_TAC_CHECKBOX = (71, 1856)

    DUMMY_TAP = (0, 1921)

    pass
