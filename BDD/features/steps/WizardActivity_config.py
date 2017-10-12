#!/usr/bin/env python
# coding:utf-8
import os, sys
import logging

from behave import given, when, then, step

from time import sleep

sys.path.append(os.path.dirname(__file__) + '/../_lib')
from android_function import finger


INIT=0
WV_GREETING=1
WV_SKIP_CHECKOUT_DATE=2
WV_SKIP_HANDYMEMBER=3
WV_SKIP_PERSONALIZED_EXPERIENCE=4
WV_PASS_PLAY_VIDEO=5
WV_PASS_TUTORIAL_IMAGE=6


# default configuration for T1
dWizardActivityPage={}
dWizardActivityPage[INIT]=u'''
    Then tap on position "0","0" using adb
        And sleep 3 seconds
        And Fail if the Text "English" not appears on screen
'''

# default for T1
dWizardActivityPage[WV_GREETING]=u'''
    # check the box next to Terms and Conds
        Then tap on position "60","1242" using adb
        And sleep 5 seconds
        And tap on button "android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"
        And sleep 3 seconds
'''

# Checkout Calendar, Checkout Calendar Skippable
dWizardActivityPage[WV_SKIP_CHECKOUT_DATE]=u'''
    # bypass checkout day currently, i should press the skip button
    # Then Wait until "When are you checking out?" appears on screen, timeout "10" seconds
    #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
    #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
    #  And tap on text "SKIP"
'''

# handy Login, handy Login Skippable
dWizardActivityPage[WV_SKIP_HANDYMEMBER] =u'''
    # Then bypass facebook registration currently, i should press the skip button
    Then Wait until Text startwith "Become a handy member!" appears on screen, timeout "10" seconds
    Then sleep 1 seconds
    #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
    #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
        And tap on text "I'll do it later"
'''

dWizardActivityPage[WV_SKIP_PERSONALIZED_EXPERIENCE]=u'''
    # Then bypass personalize experience registration currently, i should press the skip button
    # Then sleep 1 seconds
    # Then Wait until Text startwith "Let us personalize" appears on screen, timeout "10" seconds
    #   And sleep 1 seconds
    #   And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
    #   And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
    #   And tap on text "SKIP"
'''


dWizardActivityPage[WV_PASS_PLAY_VIDEO]=u'''
    # # wait a moment for video to load
    # Then Wait until Video"com.tinklabs.launcher:id/video_view" appears, timeout 60 seconds
    #   And Fail if the Video"com.tinklabs.launcher:id/video_view" not appears

    # Let's start should appears
    Then Wait until "Let's Start" appears on screen, timeout "120" seconds
        And Fail if the button "Let's Start" not appears on screen
        And tap on text "Let's Start"
'''

# Tutorial Image 1
# Tutorial Image 2
dWizardActivityPage[WV_PASS_TUTORIAL_IMAGE]=u'''
    Then Swipe "com.tinklabs.handyclock:id/gl_container" LEFT Distance "200" until "Let's start" appears on screen (max swipe "5")
        And tap on text "Let's start"
'''
