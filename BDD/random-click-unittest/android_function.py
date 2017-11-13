from time import sleep

from appium import webdriver

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

from datetime import datetime


def kill_proc(proc, timeout):
    timeout["value"] = True
    proc.kill()


def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(
        cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = {"value": False}
    timer = Timer(timeout_sec, kill_proc, [proc, timeout])
    timer.start()
    stdout, stderr = proc.communicate()
    timer.cancel()
    return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), timeout["value"]


class util():
    @staticmethod
    def initAppium(content, packageName, sActivity, sType, sPlatform, sVersion):
        desired_caps = {}
        desired_caps['platformName'] = sPlatform
        desired_caps['platformVersion'] = sVersion
        desired_caps['deviceName'] = "VZHGLMA750300169"
        # desired_caps['app'] = PATH(packageName)
        desired_caps['appPackage'] = packageName
        desired_caps['appActivity'] = sActivity
        desired_caps['deviceReadyTimeout'] = 5
        desired_caps['noReset'] = False

        # content.logger.info('findme')
        # output a appiumSession for latter use
        return webdriver.Remote(
            'http://localhost:4723/wd/hub', desired_caps)

    @staticmethod
    def getCenterOfElements(iLocX, iLocY, iWidth, iHeight):
        """
            calculate the center of elements
            :Args:
                - iLocX - location of elements (x axis)
                - iLocY - location of elements (y axis)
                - iWidth - Width of elements
                - iHeight - Height of elements

            :Result:
                - return a duple of center location (x, y)
        """
        return (
            ((iLocX + iWidth) / 2) + iLocX,
            ((iLocY + iHeight) / 2) + iLocX
        )

    # @staticmethod
    # def screencapture(sSaveToFile):
    #     """
    #         utility funtion to capture android screen in png format
    #         :Args:
    #             - appiumSession - An appium session to make the screen capture
    #             - sSaveToFile - path to save the file to
    #     """
    #     sDateString = datetime.now().strftime('%s')
    #     sPathAndroidTemp = '/sdcard'
    #     sPathAndroidScreenCapFile = sPathAndroidTemp+'.png'

    #     sAdbCmdScreenCap = 'adb shell sceencap -p %s' % sPathAndroidScreenCapFile
    #     sAdbCmdPullToPC = 'adb pull %s' % sPathAndroidScreenCapFile
    #     sAdbCmdRmScreenCapFile = 'adb shell rm %s' % sPathAndroidScreenCapFile

    #     run(sAdbCmdScreenCap, timeout_sec=10)
    #     run(sAdbCmdPullToPC, timeout_sec=10)
    #     run(sAdbCmdRmScreenCapFile, timeout_sec=10)


class finger():
    @staticmethod
    def f_TapScreen(appiumSession, sX, sY, times):
        """
            TODO: more works on tap function implementation
        """
        action = TouchAction(appiumSession)
        return action.tap().perform()

    @staticmethod
    def f_ClickElementByText(appiumSession, sElement, sText):
        # AndroidAppium is expected to be a appium session
        el = appiumSession.find_element_by_android_uiautomator(
            '''new UiSelector().className("%s").text("%s")''' % (sElement, sText))
        el.click()

    @staticmethod
    def f_ClickElementByIndex(appiumSession, sElement, iIdx):
        el = appiumSession.find_elements_by_android_uiautomator(
            '''new UiSelector().className("%s")''' % sElement)[iIdx]
        el.click()

    # def f_AndroidAnswerToOSPermission(appiumSession, sPermission_message,
    # Permission_Answer):
    # @staticmethod
    # def f_AndroidAnswerToOSPermission(appiumSession, sPermission_message, Permission_Answer):
    #     if appiumSession.find_element_by_android_uiautomator(
    #         '''new UiSelector().text("Allow MyObservatory to access this device's location?")'''
    #     ):
    #         els = appiumSession.find_elements_by_android_uiautomator(
    #             'new UiSelector().clickable(true)'
    #         )
    #         els[Permission_Answer].click()
    #     else:
    #         # TODO handling here
    #         pass

    @staticmethod
    def f_AndroidAnswerToOSPermission(appiumSession, sPermission_message, sPermission_Answer):
        """
            Answer to AndroidOS question
            :Args:
                sPermission_message: Question caption
                sPermission_Answer: String of the button would like to answer
        """
        if appiumSession.find_element_by_android_uiautomator(
            '''new UiSelector().text("%s")''' % sPermission_message
        ):
            # els = appiumSession.find_elements_by_android_uiautomator(
            #     'new UiSelector().clickable(true)'
            # )
            # els[sPermission_Answer].click()
            appiumSession.f_FindButtonWithText(
                appiumSession, sPermission_Answer)[0].click()
        else:
            # TODO handling here
            pass

    @staticmethod
    def f_AndroidAnswerToOSDialog(appiumSession, sPermission_message, sPermission_Answer):
        """
            Answer to AndroidOS question
            :Args:
                sPermission_message: Question caption
                sPermission_Answer: String of the button would like to answer
        """
        els = appiumSession.find_element_by_android_uiautomator(
            '''new UiSelector().text("%s")''' % sPermission_message
        )
        if len(els) > 0:
            # els = appiumSession.find_elements_by_android_uiautomator(
            #     'new UiSelector().clickable(true)'
            # )
            # els[sPermission_Answer].click()
            appiumSession.f_FindButtonWithText(
                appiumSession, sPermission_Answer)[0].click()
        else:
            # TODO handling here
            pass

    @staticmethod
    def f_FindTargetByXPath(appiumSession, sWidget, sProperties, sValue):
        return appiumSession.find_elements_by_xpath(
            '//%s[@%s="%s"]' % (sWidget, sProperties, sValue)
        )

    @staticmethod
    def f_FindTargetById(appiumSession, sId):
        return appiumSession.find_elements_by_id(
            '%s' % sId)

    @staticmethod
    def f_FindElementsById(appiumSession, sId):
        """
            Better naming for the function find_elements_by_id
            TODO: will replace f_FindTargetById
        """
        return appiumSession.find_elements_by_id(
            '%s' % sId)

    @staticmethod
    def f_FindTargetByClass(appiumSession, sId):
        return appiumSession.find_elements_by_class_name(
            '%s' % sId)

    @staticmethod
    def f_FindButtonWithText(appiumSession, sText):
        els = appiumSession.find_elements_by_android_uiautomator(
            'text("%s")' % sText)
        return els

    @staticmethod
    def f_FindElementsWithText(appiumSession, sText):
        """
            NOTE: TODO: for better name for f_FindButtonWithText, will phase out f_FindButtonWithText
        """
        els = appiumSession.find_elements_by_android_uiautomator(
            'text("%s")' % sText)
        return els

    @staticmethod
    def f_FindElementsContainText(appiumSession, sText):
        """
            NOTE: find elements with the text given by sText on screen
        """
        return appiumSession.find_elements_by_xpath('//android.widget.TextView[contains(@text, "%s")]' % sText)

    @staticmethod
    def f_FindElementsStartWithText(appiumSession, sText):
        els = appiumSession.find_elements_by_android_uiautomator(
            'new UiSelector().textStartsWith("%s")' % sText)
        return els

    @staticmethod
    def f_FindElementsClickable(appiumSession):
        els = appiumSession.find_elements_by_android_uiautomator(
            'new UiSelector().clickable(true)')
        return els

    @staticmethod
    def f_FindElementsWithContentDesc(appiumSession, sContentDesc):
        els = appiumSession.find_elements_by_android_uiautomator(
            'content-desc("%s")' % sContentDesc)
        return els

    @staticmethod
    def f_TapWidgetByPropertiesAndValue(appiumSession, sWidget, sProperties, sValue):
        # IDEA try to reach the clickable thing buy it properties,
        # otherwise, find it's parents
        els = finger.f_FindTargetByXPath(
            appiumSession,
            sWidget, sProperties, sValue)
        if els:
            els[0].click()

            # NOTE for debug
        else:
            raise('nothing found')
        pass

    @staticmethod
    def f_FindElementsByUiAutomator(appiumSession, sUiSelectQuery):
        """
            Wrapping for the function android_uiautomator

            :Args:
                - appiumSession - a valid appium session
                - sUiSelectQuary - an android Query by UiSelect
        """
        return appiumSession.find_elements_by_android_uiautomator(sUiSelectQuery)

    @staticmethod
    def f_GetDialogByTitle(appiumSession, sTitle):
        # return el that contain the sTitle
        pass

    @staticmethod
    def f_HandleWhatsNewDialog(appiumSession):
        # #### version update post
        #     * android.widget.ImageButton -> index 0
        # NOTE click the close button of the version update dialog

        # TODO better handling of this
        iCountDown = 5
        bContinueWait = True

        sleep(10)
        finger.f_ClickElementByIndex(
            appiumSession, 'android.widget.ImageButton', 0)

        # try:
        #     while iCountDown:
        #         if appiumSession.find_elements_by_android_uiautomator(
        #             'new UiSelector().textStartsWith("What\'s New in Version")'
        #         ):
        #             bContinueWait=False
        #         else:
        #             iCountDown-=1
        #             sleep(1)

        #         if iCountDown ==0:
        #             # TODO how to handle the interruption ?
        #             raise('cannot close dialog')

        # except Exception as e:

        #     pass

    @staticmethod
    def f_PressKey(appiumSession, sKey):
        appiumSession.press_keycode(sKey)

    # @staticmethod
    # def f_checkActivity(appiumSession, sActivity):
    #     return appiumSession.current_activ

    @staticmethod
    def f_waitForActivity(appiumSession, sTargetActivity, iSeconds, iIntervals=1):
        """
            Wait for an activity: block until target activity presents or time out.
            This is an Android-only method.

            :Agrs:
                - activity - target activity
                - timeout - max wait time, in seconds
                - interval - sleep interval between retries, in seconds
        """
        return appiumSession.wait_activity(sTargetActivity, iSeconds, iIntervals)

    # ref: https://developer.android.com/reference/android/support/test/uiautomator/UiSelector.html
    @staticmethod
    def f_FindTargetByUISelector(appiumSession, sUISelector):
        """Simple wrapper for appium UISelector class"""
        els = appiumSession.find_elements_by_android_uiautomator(sUISelector)

        return els

    @staticmethod
    def f_CheckCurrentActivity(appiumSession):
        """
            # return current activity in string form
        """
        return appiumSession.current_activity

    # @staticmethod
    # def f_Swipe(appiumSession, sDirection, sX, sY):
    #     return appiumSession.scroll()

    @staticmethod
    def f_Scroll_Elements(appiumSession, elStart, elEnd):
        """
            # simple method to perform scroll from element to element
        """

        return appiumSession.scroll(elStart, elEnd)

    @staticmethod
    def f_Swipe_Elements(appiumSession, xStart, yStart, iDistance, sDirection, iDuration):
        """
            Provide a method to swipe on screen

            :Args:
                - appiumSession - a valid appium session
                - xStart - init
        """

        (xStart, yStart) = (xStart, yStart)
        (xEnd, yEnd) = (xStart, yStart)

        if sDirection in ['UP']:
            yEnd = yStart - iDistance
        elif sDirection in ['DOWN']:
            yEnd = yStart + iDistance
        elif sDirection in ['LEFT']:
            xEnd = xStart - iDistance
        elif sDirection in ['RIGHT']:
            xEnd = xStart + iDistance
        else:
            # NOTE why i am here ?
            # FIXME: corner case not consider yet.
            pass

        return appiumSession.swipe(xStart, yStart, xEnd, yEnd, iDuration)
