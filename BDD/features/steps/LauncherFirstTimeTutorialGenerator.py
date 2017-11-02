#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint


TAP_THIS_SHOW_THE_HOTEL_DETAILS = 0
TAP_ON_THIS_ICON_TO_OPEN_THE_SIDE_BAR = 1
SCROLL_DOWN_TO_EXPLORE_ALL_THE_MAIN_FEATURES_OF_HANDY = 2
SHOP_FOR_DISCOUNTED_SOUVENIRS = 3
TOURS_AND_TICKETS_TO_MAJOR_ATTRACTIONS = 4
EXIT_TUTORIAL = 5


# IDEA: suppose a launcher with language modified

class LauncherFirstTimeTutorialConfig:
    def __init__(self, lanauage):
        # NOTE: place holder for apply language options

        pass

    TUTORIAL_STEP = {}
    TUTORIAL_STEP[TAP_THIS_SHOW_THE_HOTEL_DETAILS] = u"""
    Then sleep 5 seconds
        And Wait until "Tap this show the hotel details." appears on screen, timeout "30" seconds
        And Tap screen 1 times at CENTER
        And sleep 1 seconds
    """

    TUTORIAL_STEP[TAP_ON_THIS_ICON_TO_OPEN_THE_SIDE_BAR] = u"""
    # Tap_on_this_icon_to_open_the_side_bar
    # com.tinklabs.launcher:id/click_through means back button on the top-left
    Then sleep 5 seconds
      And Wait until "Tap on this icon to open the side bar." appears on screen, timeout "30" seconds
      And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
      And sleep 1 seconds
    """

    TUTORIAL_STEP[SCROLL_DOWN_TO_EXPLORE_ALL_THE_MAIN_FEATURES_OF_HANDY] = u"""
    # Scroll_down_to_explore_all_the_main_features_of_handy
    Then sleep 5 seconds
      And Wait until "Scroll down to explore all the main features of handy." appears on screen, timeout "30" seconds
      And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
      And sleep 1 seconds
    """

    TUTORIAL_STEP[SHOP_FOR_DISCOUNTED_SOUVENIRS] = u"""
    # Shop_for_discounted_souvenirs
    # Shop for discounted souvenirs and the hottest new products, and enjoy free delivery.
    Then Wait until "Shop for discounted souvenirs and the hottest new products, and enjoy free delivery." appears on screen, timeout "10" seconds
      And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
      And sleep 1 seconds
    """

    TUTORIAL_STEP[TOURS_AND_TICKETS_TO_MAJOR_ATTRACTIONS] = u"""
    # Tours_and_tickets_to_major_attractions
    Then Wait until Text startwith "Tours and tickets to major attractions" appears on screen, timeout "10" seconds
        And tap on Text "Tickets"
        And Wait until screen ready, timeout 30 seconds
        And sleep 5 seconds

        # NOTE as the back at upper left corner got no names. need to press the button by coordinates.
        # TODO: better naming
        # And tap on position "56","88" using adb
    """

    TUTORIAL_STEP[EXIT_TUTORIAL] = u"""
    Then press HOME button
        And Wait until screen ready, timeout 30 seconds
        And sleep 1 seconds

    # Suppose tour done
    """


class LauncherFirstTimeTutorialGenerator:
    """docstring for LauncherFirstTimeTutorialGenerator."""
    hotel_config = ''

    def __init__(self, tutorial_config, hotel_config):
        # IDEA: expecting tutorial with language preferences
        self.tutorial_steps = tutorial_config
        self.hotel_config = hotel_config

    def get_tutorial(self):
        temp = ''
        if self.hotel_config == "T1":
            temp = ''
            temp += self.tutorial_steps.TUTORIAL_STEP[TAP_THIS_SHOW_THE_HOTEL_DETAILS]
            temp += self.tutorial_steps.TUTORIAL_STEP[SHOP_FOR_DISCOUNTED_SOUVENIRS]
            temp += self.tutorial_steps.TUTORIAL_STEP[TOURS_AND_TICKETS_TO_MAJOR_ATTRACTIONS]
            temp += self.tutorial_steps.TUTORIAL_STEP[EXIT_TUTORIAL]

        elif self.hotel_config == 'M812':
            temp += self.tutorial_steps.TUTORIAL_STEP[TAP_THIS_SHOW_THE_HOTEL_DETAILS]
            temp += self.tutorial_steps.TUTORIAL_STEP[TOURS_AND_TICKETS_TO_MAJOR_ATTRACTIONS]
            temp += self.tutorial_steps.TUTORIAL_STEP[EXIT_TUTORIAL]

        else:
            logging.error('the %s is not handled ' % self.hotel_config)

        return temp
    pass
