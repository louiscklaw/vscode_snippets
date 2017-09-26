# BDT for activation flow 2.0
# reference documentation
# https://tinklabs.atlassian.net/wiki/spaces/ENG/pages/3480213/New+Activation+flow+2.0+-+31+Languages+Screen+by+Screen+Test+Plan

# -- FILE: features/com.tinklabs.activateapp
# apk:      com.tinklabs.activateapp_base.apk
# package:  com.tinklabs.activateapp
# activity: .features.wizard.WizardActivity

#{
#  "platformName": "Android",
#  "deviceName": "Android",
#  "appPackage": "com.tinklabs.launcher",
#  "appActivity": "com.tinklabs.launcher.features.main.activity.LauncherActivity"
#}

Feature: display terms and conditions
  Background: scratch background
    Given setup an android as below
    | Package                  | Activity                        |  platform | type  |version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity |  Android  | phone |7.0     |
      And Wait for "Waiting for network connection..." ("10" countdown)
      And Wait for "Initializing..." ("20" countdown)
      And Wait for "checking for update..." ("10" countdown)
      And sleep 20 seconds

  Scenario: display Privacy and Security at wv_AskForCheckoutDate
    When Reach "ask for checkout date" page in WizardActivity by skip

    Then Fail if the Text "Why do we need this?" not appears on screen
      And tap on Text "Why do we need this?"

    Then Fail if the Text "For your privacy and security" not appears on screen
      And Fail if the Text "GOT IT" not appears on screen

    # NOTE to check if "GOT IT" can close the windows
    Given tap on Text "GOT IT"
    Then Fail if the Text "For your privacy and security" is appears on screen
      And Fail if the Text "GOT IT" is appears on screen
