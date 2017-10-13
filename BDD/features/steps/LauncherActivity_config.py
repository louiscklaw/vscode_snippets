#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint


class LauncherActivity_config:
    ERASE_ALL_DATA = ''
    LEFT_DRAWER_ERASE_DATA = 'Erase All Data'

    ERASE_DATA_BUTTON_RESOURCE_ID = u"com.tinklabs.activateapp:id/mira_factory_reset"
    CANCEL_BUTTON_RESOURCE_ID = u"com.tinklabs.activateapp:id/cancel"

    ERASE_DATA_CONFIRMATION_YES = u'android:id/button1'
    ERASE_DATA_CONFIRMATION_NO = u'android:id/button2'

    def __init__(self, device):
        if device == "T1":
            self.ERASE_ALL_DATA = 'Erase Data'
            self.LEFT_DRAWER_ERASE_DATA = 'Erase Data'
        if device == "M812":
            self.ERASE_ALL_DATA = 'Erase Data'
            self.LEFT_DRAWER_ERASE_DATA = 'Erase All Data'
