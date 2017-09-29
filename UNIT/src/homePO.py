import os
import sys
srcParentFolder = os.path.dirname(os.path.normpath(sys.path[0]))
unitParentFoler = os.path.dirname(os.path.normpath(srcParentFolder))
sys.path.append(unitParentFoler)
from UNIT.res import homeEle
import UTIL.utils as utils

class homePO:
    def __init__(self, PageObject):
        self.PO = PageObject

    def goToCallTab(self):
        try:
            callEle = self.PO.getEleByTextInMultiEleByID(
                homeEle.buttomTab['rid'], homeEle.buttomTab['call'], 'get Call element'
            )
            callEle.click()
        except:
            utils.logv2('Go to Call Tab', 'Fail')
            raise

    def goToHomeTab(self):
        try:
            callEle = self.PO.getEleByTextInMultiEleByID(
                homeEle.buttomTab['rid'], homeEle.buttomTab['home'], 'get Home element'
            )
            callEle.click()
        except:
            utils.logv2('Go to Home Tab', 'Fail')
            raise

    def goToAppsTab(self):
        try:
            callEle = self.PO.getEleByTextInMultiEleByID(
                homeEle.buttomTab['rid'], homeEle.buttomTab['app'], 'get Apps element'
            )
            callEle.click()
        except:
            utils.logv2('Go to Apps Tab', 'Fail')
            raise

    def goToCityGuideTab(self):
        try:
            callEle = self.PO.getEleByTextInMultiEleByID(
                homeEle.buttomTab['rid'], homeEle.buttomTab['cityGuide'], 'get City Guide element'
            )
            callEle.click()
        except:
            utils.logv2('Go to City Guide Tab', 'Fail')
            raise

    def goToTicketsTab(self):
        try:
            callEle = self.PO.getEleByTextInMultiEleByID(
                homeEle.buttomTab['rid'], homeEle.buttomTab['tickets'], 'get Tickets element'
            )
            callEle.click()
        except:
            utils.logv2('Go to Tickets Tab', 'Fail')
            raise