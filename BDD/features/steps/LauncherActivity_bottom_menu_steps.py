
from behave import given, when, then, step
import os
import sys

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

# @then(u'6 buttons should appears at the bottom')
@step(u'Fail if "{ButtonText}" button not appear at the position given by "{Position}"')
def fail_if_button_not_appear_at_the_position(context, ButtonText, Position, sId):
    # basic components of a button
    sUiSelectorButtons='new UiSelector().resourceId("%s")' % sId
    UiSelectorButtonText = 'new UiSelector().text("%s")' % ButtonText

    # button group
    sUiSelectForFiveButton = "%s.childSelector(%s)" % (sUiSelectorButtons, UiSelectorButtonText)

    els=finger.f_FindTargetByUISelector(context.appiumSession, sUiSelectForFiveButton)
    # els=els[int(Position)-1].f_FindTargetByUISelector(context.appiumSession, ButtonText)

    if len(els) != 1 :
        assert False

    pass

@step(u'Fail if buttons on the list below not appear at the position with id "{sId}"')
def step_impl(context, sId):
    for row in context.table:
        fail_if_button_not_appear_at_the_position(context, row['button'],row['position'], sId)
