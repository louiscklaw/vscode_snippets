#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

# logging.basicConfig(level=logging.debug)

INIT = 0
WV_GREETING = 1
WV_SKIP_CHECKOUT_DATE = 2
WV_SKIP_HANDYMEMBER = 3
WV_SKIP_PERSONALIZED_EXPERIENCE = 4
WV_PASS_PLAY_VIDEO = 5
WV_PASS_TUTORIAL_IMAGE = 6


class WizardActivityPageConfig:
    Config = {}

    def __init__(self, device):
        if device == 'T1':
            self.Config['DUMMY_TAP_X'] = '0'
            self.Config['DUMMY_TAP_Y'] = '0'

            self.Config['GREETING_TAC_CHECKBOX_X'] = u"60"
            self.Config['GREETING_TAC_CHECKBOX_Y'] = u"1242"

            # page specific text/label
            self.Config['SKIP'] = u'SKIP'
            self.Config['I_LL_DO_IT_LATER'] = u"I'll do it later"
            self.Config['LET_S_START'] = u"Let's Start"
            self.Config['TUTORIAL_IMAGE_LET_S_START'] = u"Let's start"

            # left_drawer / side menu
            self.Config['LEFT_DRAWER_ERASE_DATA'] = u"Erase Data"

        if device == 'M812':
            self.Config['DUMMY_TAP_X'] = '0'
            self.Config['DUMMY_TAP_Y'] = '0'

            self.Config['GREETING_TAC_CHECKBOX_X'] = u"71"
            self.Config['GREETING_TAC_CHECKBOX_Y'] = u"1856"

            # page specific text/label
            self.Config['SKIP'] = u'SKIP'
            self.Config['I_LL_DO_IT_LATER'] = u"I'll do it later"
            self.Config['LET_S_START'] = u"Let's Start"
            self.Config['TUTORIAL_IMAGE_LET_S_START'] = u"Let's start"

            # left_drawer / side menu
            self.Config['LEFT_DRAWER_ERASE_DATA'] = u"Erase Data"


class WizardActivityPageGenerator:
    # TODO: consider about language
    # TODO: consider about resolution
    # TODO: consider about device

    Page = {}

    def __init__(self, page_config):

        # NOTE: device level config
        self.Page = page_config.Config

        # NOTE: page level config
        self.Page['GREETING_RIGHT_ARROW'] = u'"android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"'

    def get_page(self, id_page):

        if id_page == INIT:
            return u'''
                Then tap on position "%(DUMMY_TAP_X)s","%(DUMMY_TAP_Y)s" using adb
                    And sleep 3 seconds
                    And Fail if the Text "English" not appears on screen
            ''' % self.Page

        if id_page == WV_GREETING:
            return u'''
                # check the box next to Terms and Conds
                Then tap on position "%(GREETING_TAC_CHECKBOX_X)s","%(GREETING_TAC_CHECKBOX_Y)s" using adb
                    And sleep 5 seconds
                    And tap on button %(GREETING_RIGHT_ARROW)s
                    And sleep 3 seconds
            ''' % self.Page

        if id_page == WV_SKIP_CHECKOUT_DATE:
            return u'''
                # bypass checkout day currently, i should press the skip button
                Then Wait until "When are you checking out?" appears on screen, timeout "10" seconds
                #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
                #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
                    And tap on text "%(SKIP)s"
            ''' % self.Page

        if id_page == WV_SKIP_HANDYMEMBER:
            return u'''
                # Then bypass facebook registration currently, i should press the skip button
                Then Wait until Text startwith "Become a handy member!" appears on screen, timeout "10" seconds
                Then sleep 1 seconds
                #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
                #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
                    And tap on text "%(I_LL_DO_IT_LATER)s"
            ''' % self.Page

        if id_page == WV_SKIP_PERSONALIZED_EXPERIENCE:
            return u'''
                # Then bypass personalize experience registration currently, i should press the skip button
                # Then sleep 1 seconds
                Then Wait until Text startwith "Let us personalize" appears on screen, timeout "10" seconds
                    And sleep 1 seconds
                #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
                #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
                    And tap on text "%(SKIP)s"
            ''' % self.Page

        if id_page == WV_PASS_PLAY_VIDEO:
            return u'''
                # Let's start should appears
                Then Wait until "%(LET_S_START)s" appears on screen, timeout "120" seconds
                    And tap on text "%(LET_S_START)s"
            ''' % self.Page

            # Tutorial Image 1
            # Tutorial Image 2
        if id_page == WV_PASS_TUTORIAL_IMAGE:
            return u'''
                Then press HOME button
                Then Wait until "resource-id" "com.tinklabs.launcher:id/ivBackground" appears on screen, timeout 60 seconds
                Then Swipe "com.tinklabs.launcher:id/ivBackground" LEFT Distance "200" until "Let's start" appears on screen (max swipe "10")
                    And tap on text "%(TUTORIAL_IMAGE_LET_S_START)s"
            ''' % self.Page


class WizardActivityPage:
    dWizardActivityPage = {}

    # Wizard screen
    INIT = 0
    WV_GREETING = 1
    WV_SKIP_CHECKOUT_DATE = 2
    WV_SKIP_HANDYMEMBER = 3
    WV_SKIP_PERSONALIZED_EXPERIENCE = 4
    WV_PASS_PLAY_VIDEO = 5
    WV_PASS_TUTORIAL_IMAGE = 6

    # NOTE: default parameters
    ELEMENTS = {}
    ELEMENTS['GREETING_RIGHT_ARROW'] = u'"android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"'

    ELEMENTS['GREETING_TAC_CHECKBOX_X'] = u"60"
    ELEMENTS['GREETING_TAC_CHECKBOX_Y'] = u"1242"

    ELEMENTS['DUMMY_TAP_X'] = u"0"
    ELEMENTS['DUMMY_TAP_Y'] = u"0"

    # page specific text/label
    ELEMENTS['SKIP'] = u'SKIP'
    ELEMENTS['I_LL_DO_IT_LATER'] = u"I'll do it later"
    ELEMENTS['LET_S_START'] = u"Let's Start"
    ELEMENTS['TUTORIAL_IMAGE_LET_S_START'] = u"Let's start"

    # left_drawer / side menu
    ELEMENTS['LEFT_DRAWER_ERASE_DATA'] = u"Erase All Data"

    dWizardActivityPage[INIT] = u'''
        Then tap on position "%(DUMMY_TAP_X)s","%(DUMMY_TAP_Y)s" using adb
            And sleep 3 seconds
            And Fail if the Text "English" not appears on screen
    ''' % ELEMENTS

    dWizardActivityPage[WV_GREETING] = u'''
        # check the box next to Terms and Conds
        Then tap on position "%(GREETING_TAC_CHECKBOX_X)s","%(GREETING_TAC_CHECKBOX_Y)s" using adb
            And sleep 5 seconds
            And tap on button %(GREETING_RIGHT_ARROW)s
            And sleep 3 seconds
    ''' % ELEMENTS

    dWizardActivityPage[WV_SKIP_CHECKOUT_DATE] = u'''
        # bypass checkout day currently, i should press the skip button
        Then Wait until "When are you checking out?" appears on screen, timeout "10" seconds
        #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
        #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
            And tap on text "%(SKIP)s"
    ''' % ELEMENTS

    dWizardActivityPage[WV_SKIP_HANDYMEMBER] = u'''
        # Then bypass facebook registration currently, i should press the skip button
        Then Wait until Text startwith "Become a handy member!" appears on screen, timeout "10" seconds
        Then sleep 1 seconds
        #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
        #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
            And tap on text "%(I_LL_DO_IT_LATER)s"
    ''' % ELEMENTS

    dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE] = u'''
        # Then bypass personalize experience registration currently, i should press the skip button
        # Then sleep 1 seconds
        Then Wait until Text startwith "Let us personalize" appears on screen, timeout "10" seconds
            And sleep 1 seconds
        #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
        #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
            And tap on text "%(SKIP)s"
    ''' % ELEMENTS

    dWizardActivityPage[WV_PASS_PLAY_VIDEO] = u'''
        # Let's start should appears
        Then Wait until "%(LET_S_START)s" appears on screen, timeout "120" seconds
            And tap on text "%(LET_S_START)s"
    ''' % ELEMENTS

    # Tutorial Image 1
    # Tutorial Image 2
    dWizardActivityPage[WV_PASS_TUTORIAL_IMAGE] = u'''
        Then press HOME button
        Then Wait until "resource-id" "com.tinklabs.launcher:id/ivBackground" appears on screen, timeout 60 seconds
        Then Swipe "com.tinklabs.launcher:id/ivBackground" LEFT Distance "200" until "Let's start" appears on screen (max swipe "10")
            And tap on text "%(TUTORIAL_IMAGE_LET_S_START)s"
    ''' % ELEMENTS
