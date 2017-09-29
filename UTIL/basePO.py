import os
import time
import utils
import sys
# from appium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

screenDir = os.path.dirname(os.path.normpath(sys.path[0]))
class PageObject:
    def __init__(self,device):
        self.driver = device
        if not os.path.exists(self.screenDir):
            os.makedirs(self.screenDir)

    def findByID(self, id, log='', timeout=3):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.ID, id))
            )
            utils.logv2(log, 'Done')
            return element
        except:
            utils.logv2(log, 'Fail')
            raise

    def getEleByXpath(self, xpath):
        ele = self.driver.find_element(By.XPATH, xpath)
        return ele

    def findByXpath(self, xpath, log='', timeout=3):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            utils.logv2(log, 'Done')
            return element
        except:
            utils.logv2(log, 'Fail')
            raise

    def findByDesc(self, desc, log='', timeout=3):
        try:
            selector = 'new UiSelector().description(\"' + desc + '\")'
            element = self.driver.find_element_by_android_uiautomator(selector)
            utils.logv2(log, 'Done')
            return element
        except:
            utils.logv2(log, 'Fail')
            raise

    def findByText(self, text, log='', timeout=3):
        try:
            selector = 'new UiSelector().text(\"' + text + '\")'
            element = self.driver.find_element_by_android_uiautomator(selector)
            utils.logv2(log, "Done")
            return element
        except:
            utils.logv2(log, 'Fail')
            raise


    def isEleClickable(self, rid, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.ID, rid)))
            return True
        except TimeoutException:
            print("Check element " + str(rid) + " clickable fail.")
            return False

    def isElePresence(self, rid, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, rid)))
            return True
        except TimeoutException:
            print("Check element " + str(rid) + " presence fail.")
            return False

    def ieEleVisible(self, rid, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, rid)))
            return True
        except TimeoutException:
            print("Check element " + str(rid) + " visible fail.")
            return False


    def scrollToByID(self, rid):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().resourceId(\"' + rid + '\").instance(0));')
            return True
        except TimeoutException:
            print("Scroll to element " + str(rid) + " Timeout.")
            return False

    def scrollToFindByID(self, id, log=''):
        try:
            selector = 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().resourceId(\"' + id + '\").instance(0));'
            element = self.driver.find_element_by_android_uiautomator(selector)
            utils.logv2(log, "Done")
            return element
        except:
            utils.logv2(log, "Fail")
            raise

    def scrollToFindByText(self, text, log=''):
        try:
            selector = 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text(\"' + text + '\").instance(0));'
            element = self.driver.find_element_by_android_uiautomator(selector)
            utils.logv2(log, "Done")
            return element
        except:
            utils.logv2(log, "Fail")
            raise

    def isNotMatch(self, resultA, resultB, str=""):
        try:
            if(resultA != resultB):
                utils.logv2(str, "Done")
                return True
            else:
                utils.logv2(str, "FAIL")
                return False
        except:
            utils.logv2(str, "FAIL")
            raise

    def isMatch(self, stringA, stringB):
        if stringA == stringB:
            return True
        else:
            utils.log(stringA + " is not match " + stringB)
            return False


    def screenshot(self, name):
        screenshot_name = str(time.strftime("%Y%m%d%H%M%S")) + "_" + name + ".png"
        utils.log("Taking screenshot: " + screenDir + "/" + screenshot_name)
        # on Android, switching context to NATIVE_APP for screenshot
        # taking to get screenshots also stored to Testdroid Cloud
        # device run view. After screenshot switching back to
        # WEBVIEW. Works ok for Safari too.
        orig_context = self.driver.current_context
        self.driver.switch_to.context("NATIVE_APP")
        self.driver.save_screenshot(screenDir + "/" + screenshot_name)
        # only change context if originally context was WEBVIEW
        if orig_context not in self.driver.current_context:
            self.driver.switch_to.context("WEBVIEW")
        # self.screenshot_count += 1

    def test(self):
        print(screenDir)