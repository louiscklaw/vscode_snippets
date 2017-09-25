
from behave import given, when, then, step
import os
import sys

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

@step(u'finish LauncherActivity tutorial')
def step_impl(context):
    context.execute_steps(u'''
    # Tap_this_show_the_hostel_details
    Then Fail if the "Tap this show the hotel details." not appears on screen
      and Tap screen 1 times at CENTER

    # Tap_on_this_icon_to_open_the_side_bar
    # com.tinklabs.launcher:id/click_through means back button on the top-left
    Then Fail if the "Tap on this icon to open the side bar." not appears on screen
      and tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"

    # Scroll_down_to_explore_all_the_main_features_of_handy
    Then Fail if the "Scroll down to explore all the main features of handy." not appears on screen
      and tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
    ''')
