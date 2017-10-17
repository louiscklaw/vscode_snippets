
from behave import given, when, then, step
import os
import sys
import logging

sys.path.append(os.path.dirname(__file__) + '/../_lib')
from android_function import finger
from android_function import util

from time import sleep

from LauncherFirstTimeTutorialGenerator import *
from LauncherActivity_config import *


@step(u'Skip the 1st time tutorial by launcher')
def step_impl(context):
    """
        just to skip the 1st time tutorial from launcher
    """

    # TODO: implement pass/fail option in the script
    #   GRAMMER:
    #       {Skip/Pass} the 1st time tutorial by launcher
    if hasattr(context, 'device'):
        tutorial_config = LauncherFirstTimeTutorialConfig('en_US')
        tutorial_route = LauncherFirstTimeTutorialGenerator(
            tutorial_config, context.device)
        context.execute_steps(tutorial_route.get_tutorial())
    else:
        logging.error('the device is not handled')
        assert False, 'the device is not handled'
    pass


@step(u'Press {sDialogAnswer} in {sDialogTitle} Dialog, timeout {sDialogTimeout} seconds')
def step_impl(context, sDialogAnswer, sDialogTitle, sDialogTimeout):
    """
        Handle answering of the dialog
        :Args:
            - sAns - Answer to the dialog YES/NO
            - sTitle - The title of the dialog
    """

    context.execute_steps(u'''
        Then Wait until "%s" appears on screen, timeout "%s" seconds
            And tap on text "%s"
    ''' % (sDialogTitle, sDialogTimeout, sDialogAnswer))


@step(u'Perform and {confirm} erase data in Erase data screen')
def step_impl(context, confirm):
    """
        perform erase data in erase data screen
        :Args:
            - confirm - "confirm/don't confirm",  Erase data, press yes after pressing erase data.

        TODO: AdHoc function, to be developed
        NOTE:
            - sConfirmationDialogShowTime - means the time between clicking "ERASE DATA" in erase data screen and the pop-up for dialog for confirmation
    """
    LauncherActivityConfig = LauncherActivity_config(context.device)

    dSettings = {}
    dSettings['confirmation_dialog_show_timeout'] = '30'
    dSettings['left_drawer_erase_data'] = LauncherActivityConfig.LEFT_DRAWER_ERASE_DATA
    dSettings['erase_data_button'] = LauncherActivityConfig.ERASE_ALL_DATA
    dSettings['erase_data_button_resource_id'] = LauncherActivityConfig.ERASE_DATA_BUTTON_RESOURCE_ID

    dSettings['erase_data_confirmation_yes'] = LauncherActivityConfig.ERASE_DATA_CONFIRMATION_YES
    dSettings['erase_data_confirmation_no'] = LauncherActivityConfig.ERASE_DATA_CONFIRMATION_NO

    logging.debug('i supposed to click the "Erase Data" on left_drawer')

    context.execute_steps(u'''
        # Tap on the Erase Data option on left drawer
        Then tap on text "%(left_drawer_erase_data)s"

          # the screen pop-up with erase data caption
          And Wait until "Erase Data" appears on screen, timeout "%(confirmation_dialog_show_timeout)s" seconds
    ''' % dSettings)
    if confirm in ['confirm']:
        logging.debug('i supposed clicking "YES" to confirm ERASE DATA')
        context.execute_steps(u'''
            # NOTE given that i want to erase data
            # i am standing on the "Erase Data" screen

            # The erase data / cancel selection at the bottom
            # Then Wait until "%(erase_data_button)s" appears on screen, timeout "30" seconds
            #   And tap on text "%(erase_data_button)s"

            Then Wait until "resource-id" "%(erase_data_button_resource_id)s" appears on screen, timeout 60 seconds
              And tap on button "android.widget.Button":"resource-id":"%(erase_data_button_resource_id)s"

              And Wait until "Confirmation" appears on screen, timeout "%(confirmation_dialog_show_timeout)s" seconds

            # And tap on text "YES"
              And tap on button "android.widget.Button":"resource-id":"%(erase_data_confirmation_yes)s"


        ''' % dSettings
                              )
    elif confirm in ["don't confirm"]:
        logging.debug('i supposed clicking "No" to confirm ERASE DATA')
        context.execute_steps(u'''
            # NOTE given that i erase data, and then cancel/revert
            Then Wait until "ERASE DATA" appears on screen, timeout "5" seconds
              And tap on text "ERASE DATA"
              And Wait until "Confirmation" appears on screen, timeout "%(confirmation_dialog_show_timeout)s" seconds

              # And tap on text "NO"
              And tap on button "android.widget.Button":"resource-id":"%(erase_data_confirmation_no)s"

        ''' % dSettings)
    pass


@step(u'In launcher side menu, Erase data')
def step_impl(context):
    LauncherActivityConfig = LauncherActivity_config(context.device)

    logging.debug('i am supposed to be tapping "Erase data" from left_drawer')
    context.execute_steps(u'''
        # Given In launcher side menu, Erase data
        Then press HOME button
          And Wait until screen ready, timeout 30 seconds
          And sleep 3 seconds

        Then tap hamburger button on launcher
          And Wait until "Taxi Card" appears on screen, timeout "10" seconds
          And Swipe the menu UP until "%s" appears on screen (max swipe "15")

          # select Erase Data in menu
          And Perform and confirm erase data in Erase Data screen
    ''' % LauncherActivityConfig.LEFT_DRAWER_ERASE_DATA)
    pass


@step(u'random click for an hour')
def step_impl(context):
    logging.debug('i am supposed to be a random click for an hour')
    pass


@step(u'tap hamburger button on launcher')
def step_impl(context):
    """
        tap the menu button on the top left in launcher
        resource-id: com.tinklabs.launcher:id/menu_button

        TODO: documenation here, generalization
    """

    context.execute_steps(u'''
      Then Wait until "resource-id" "com.tinklabs.launcher:id/menu_button" appears on screen, timeout 60 seconds

        # And tap on button "android.widget.ImageView":"resource-id":"com.tinklabs.launcher:id/menu_button"

        # As of 7.0, the hamburger menu button is a FrameLayout instead of ImageView.
        And tap on button "android.widget.FrameLayout":"resource-id":"com.tinklabs.launcher:id/menu_button"
    ''')

    pass


@step(u'Scroll "{element1}" to "{element2}"')
def step_scroll_elements(context, element1, element2):
    """
        scroll until the target text appears
        :Args:
            element1: starting element
            element2: ending element (objective)
    """

    finger.f_Scroll(
        context.appiumSession,
        element1, element2
    )
    pass


# @then(u'Swipe the menu UP until "Erase Data" appears on screen (countdown "15")')
@step(u'Swipe the menu {sDirection} until "{sText}" appears on screen (max swipe "{countdown}")')
def step_impl(context, sText, countdown, sDirection):
    """
        perform swipe action on the target until Text appears
        NOTE:
            The left menu/draw menu is given by: resource-id="com.tinklabs.launcher:id/left_drawer_list"
            The items on the menu temporary defined as resource-id="com.tinklabs.launcher:id/tab_item[array]" under menu'

            That means:
                new UiSelector().resourceId("com.tinklabs.launcher:id/left_drawer_list").childSelector(new UiSelector().resourceId("com.tinklabs.launcher:id/tab_item))

        TODO: i need tidy up/better optimize
    """
    bTextFound = False
    iCountdown = int(countdown)
    iNumberOfElementFound = len(
        finger.f_FindElementsWithText(context.appiumSession, sText))
    sLeftDrawer = "com.tinklabs.launcher:id/left_drawer_list"
    sMenuItem = "com.tinklabs.launcher:id/tab_item"
    # sUiQuery            = 'new UiSelector().resourceId("%s").childSelector(new UiSelector().resourceId("%s"))' % (sLeftDrawer, sMenuItem)
    sUiQuery = 'new UiSelector().resourceId("%s")' % (sMenuItem)

    if len(finger.f_FindElementsWithText(context.appiumSession, sText)) > 0:
        # NOTE given that the sText is already appears in the screen
        pass
    else:
        for i in range(1, iCountdown):
            sleep(1)
            if len(finger.f_FindElementsWithText(context.appiumSession, sText)) > 0:
                # NOTE: sText Found
                bTextFound = True
                break

            else:
                # NOTE: sText not found, go swipe {sDirection} and check please
                finger.f_Swipe_Elements(
                    context.appiumSession, 180, 900, 600, sDirection, 1000)

    if bTextFound:
        # NOTE do something when found ?
        pass
    else:
        # NOTE do something when not found ?
        pass

    pass


@step(u'Swipe "{sResourceId}" {sDirection} Distance "{sDistance}" until text containing "{sText}" appears on screen (max swipe "{sCountdown}")')
def step_impl(context, sResourceId, sDirection, sDistance, sText, sCountdown):
    """
        perform swip on target element, find the text containing given by sText is appears on screen or not. stop on the text appears on screen
    """
    iDistance = int(sDistance)
    iCountdown = int(sCountdown)
    bTextFound = False

    els = finger.f_FindElementsById(context.appiumSession, sResourceId)
    if len(els) > 0:
        el = els[0]

        (iCenterX, iCenterY) = util.getCenterOfElements(
            el.location['x'],
            el.location['y'],
            el.size['width'],
            el.size['height']
        )
        # logging.debug('iCenterX:%d' % iCenterX)
        # logging.debug('iCenterY:%d' % iCenterY)

        if len(finger.f_FindElementsContainText(context.appiumSession, sText)) > 0:
            # NOTE given thatt the sText is already appears in the screen
            pass
        else:
            for i in range(1, iCountdown):
                context.execute_steps(u'''
                    Then Wait until screen ready, timeout 30 seconds
                ''')

                if len(finger.f_FindElementsContainText(context.appiumSession, sText)) > 0:
                    # NOTE: sText Found
                    bTextFound = True
                    break

                else:
                    # NOTE: sText not found, go swipe {sDirection} and check please
                    finger.f_Swipe_Elements(
                        context.appiumSession, iCenterX, iCenterY, iDistance, sDirection, 300)

        if bTextFound:
            # NOTE do something when found ?
            pass
        else:
            # NOTE do something when not found ?
            pass
        pass
    else:
        logging.debug('len of elements %d' % len(els))
        assert False, 'cannot find the element wanted: %s' % sText


@step(u'Swipe "{sResourceId}" {sDirection} Distance "{sDistance}" until "{sText}" appears on screen (max swipe "{sCountdown}")')
def step_impl(context, sResourceId, sDirection, sDistance, sText, sCountdown):
    """
        perform swip on target element given by sResourceId
    """
    iDistance = int(sDistance)
    iCountdown = int(sCountdown)
    bTextFound = False

    els = finger.f_FindElementsById(context.appiumSession, sResourceId)
    if len(els) > 0:
        el = els[0]

        (iCenterX, iCenterY) = util.getCenterOfElements(
            el.location['x'],
            el.location['y'],
            el.size['width'],
            el.size['height']
        )

        if len(finger.f_FindElementsWithText(context.appiumSession, sText)) > 0:
            # NOTE given thatt the sText is already appears in the screen
            logging.debug('the wanted text is already found, no need to swipe')
            pass
        else:
            # NOTE text not in the screen, need swipe
            logging.debug('cannot find the target text %s, start swipe' % sText)
            for i in range(1, iCountdown):
                context.execute_steps(u'''
                    Then Wait until screen ready, timeout 30 seconds
                ''')

                if len(finger.f_FindElementsWithText(context.appiumSession, sText)) > 0:
                    # NOTE: sText Found
                    bTextFound = True
                    break

                else:
                    # NOTE: sText not found, go swipe {sDirection} and check please
                    finger.f_Swipe_Elements(
                        context.appiumSession, iCenterX, iCenterY, iDistance, sDirection, 300)

        if bTextFound:
            # NOTE do something when found ?
            logging.debug('the wanted text found after swipe')
            pass
        else:
            logging.debug('the wanted text cannot found after swipe')
            pass
        pass
    else:
        logging.debug('len of elements %d' % len(els))
        assert False, 'cannot find the element by resource-id %s' % sResourceId


@then(u'type "{sText}" in "{sResourceId}"')
def step_impl(context, sText, sResourceId):
    logging.debug(u'I am supposed to type "' + sText + '" in ' + sResourceId)

    els = finger.f_FindElementsById(context.appiumSession, sResourceId)
    if els > 0:
        els[0].send_keys(sText)
    else:
        logging.debug('wanted %s not found' % sResourceId)
        assert False


# # NOTE left drawer = hamburger + menu
# @step(u'Scroll the menu until "{sText}" appears on screen (countdown "{countdown}")')
# def step_impl(context, sText, countdown):
#     """
#         perform swipe action on the target until Text appears
#         NOTE:
#             The left menu/draw menu is given by: resource-id="com.tinklabs.launcher:id/left_drawer_list"
#             The items on the menu temporary defined as resource-id="com.tinklabs.launcher:id/tab_item[array]" under menu'

#             That means:
#                 new UiSelector().resourceId("com.tinklabs.launcher:id/left_drawer_list").childSelector(new UiSelector().resourceId("com.tinklabs.launcher:id/tab_item))
#     """
#     bTextFound            = False
#     iCountdown            = int(countdown)
#     iNumberOfElementFound = len(finger.f_FindElementsWithText(context.appiumSession, sText))
#     sLeftDrawer           = "com.tinklabs.launcher:id/left_drawer_list"
#     sMenuItem             = "com.tinklabs.launcher:id/tab_item"
#     # sUiQuery            = 'new UiSelector().resourceId("%s").childSelector(new UiSelector().resourceId("%s"))' % (sLeftDrawer, sMenuItem)
#     sUiQuery              = 'new UiSelector().resourceId("%s")' % ( sMenuItem)

#     # dMenu = {
#     #     'sLeftDrawer':'new UiSelector().resourceId("android:id/list")',
#     #     'sMenuItem':'new UiSelector().resourceId("android:id/text1")'
#     # }

#     # # sTargetUiSelector = ('%(sLeftDrawer)s.childSelector(%(sMenuItem)s)' % dMenu)
#     # sTargetUiSelector = ('%(sLeftDrawer)s.childSelector(%(sMenuItem)s)' % dMenu)


#     dMenu = {
#         'sLeftDrawer':'new UiSelector().className("android.widget.LinearLayout")',
#         'sMenuItem':'new UiSelector().resourceId("com.tinklabs.launcher:id/tab_item")'
#     }

#     # sTargetUiSelector = ('%(sLeftDrawer)s.childSelector(%(sMenuItem)s)' % dMenu)
#     sTargetUiSelector = ('%(sLeftDrawer)s.childSelector(%(sMenuItem)s)' % dMenu)

#     els = finger.f_FindElementsById(context.appiumSession, 'com.tinklabs.launcher:id/tab_item')
#     logging.debug(len(els))

#     # NOTE the menu is given by
#     if len(els) > 1 :
#         for i in range(1, iCountdown+1):
#             sleep(0.5)
#             if iNumberOfElementFound > 0:
#                 bTextFound = True
#                 break
#             else:
#                 logging.debug('length of elements %d' % len(els))
#                 finger.f_Scroll_Elements(context.appiumSession, els[2], els[1])
#     else:
#         logging.debug('no elements found')

#     if bTextFound:
#         # NOTE do something when found ?
#         pass
#     else:
#         # NOTE do something when not found ?
#         pass

#     pass


# @step(u'Pass the 1st tutorial in launcher')
# def step_impl(context):
#     context.execute_steps(u'''
#         # to check and pass the greeting messasge
#         Then Fail if the "Tap this show the hotel details." not appears on screen
#           And Tap screen 1 times at CENTER
#           And sleep 1 seconds

#         # Tap_on_this_icon_to_open_the_side_bar
#         # com.tinklabs.launcher:id/click_through means back button on the top-left
#         Then Fail if the "Tap on this icon to open the side bar." not appears on screen
#           And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
#           And sleep 1 seconds

#         # Scroll_down_to_explore_all_the_main_features_of_handy
#         Then Fail if the "Scroll down to explore all the main features of handy." not appears on screen
#           And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
#           And sleep 1 seconds

#         # Shop_for_discounted_souvenirs
#         Then Fail if the "Shop for discounted souvenirs and the hottest new products, and enjoy free delivery." not appears on screen
#           And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
#           And sleep 1 seconds

#         # Tours_and_tickets_to_major_attractions
#         Then Fail if the "Tours and tickets to major attractions - all available here at a discount.Tours and tickets to major attractions - all available here at a discount." not appears on screen
#           And tap on button "android.view.View":"resource-id":"com.tinklabs.launcher:id/click_through"
#           And sleep 1 seconds
#     ''')
