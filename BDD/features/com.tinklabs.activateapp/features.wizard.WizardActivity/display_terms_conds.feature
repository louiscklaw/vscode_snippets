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
      And sleep 20 seconds

  @wip
  Scenario: display terms and conditions at wv_handy_member
    When Reach "Become a handy member" page in WizardActivity by skip

    Then Fail if the "By continuing, you agree to our Terms & Conditions" not appears on screen
      And tap on Text "By continuing, you agree to our Terms & Conditions"
      And sleep 10 seconds

    Then Fail if the content-desc "TERMS & CONDITIONS OF USE OF handy DEVICE AND PRIVACY POLICY" not appears on screen
    Then Fail if "GOT IT" not appears on screen

  Scenario: display terms and conditions at wv_login_to_account
    Given Reach "Log in to yo your handy account" page

    Then Fail if the "By continuing, you agree to our Terms & Conditions" not appears on screen
      And tap on Text "By continuing, you agree to our Terms & Conditions"

    Then Fail if the content-desc "TERMS & CONDITIONS OF USE OF handy DEVICE AND PRIVACY POLICY" not appears on screen
    Then Fail if "GOT IT" not appears on screen

  Scenario: display terms and conditions at wv_become_member
    Given Reach "Become a handy member" page

    Then Fail if the "By continuing, you agree to our Terms & Conditions" not appears on screen
      And tap on Text "By continuing, you agree to our Terms & Conditions"

    Then Fail if the content-desc "TERMS & CONDITIONS OF USE OF handy DEVICE AND PRIVACY POLICY" not appears on screen
    Then Fail if "GOT IT" not appears on screen

  Scenario: display terms and conditions at very first page
    Given press HOME button

    Then Fail if the Text "By continuing, you agree to our Terms & Conditions" not appears on screen
      And tap on Text "By continuing, you agree to our Terms & Conditions"
      And sleep 99 seconds

    Then Fail if the content-desc "TERMS & CONDITIONS OF USE OF handy DEVICE AND PRIVACY POLICY" not appears on screen
      And Fail if the Text "GOT IT" not appears on screen

    Then tap on Text "GOT IT"
