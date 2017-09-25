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

Feature: WizardAcitivity passing through happy flow
  Background: scratch background
    Given setup an android as below
    | Package                  | Activity                        |  platform | type  |version |
    | com.tinklabs.activateapp | .features.wizard.WizardActivity |  Android  | phone |7.0     |
      And Wait until "English" appears on screen, timeout "180" seconds

  Scenario: Sanity test for Wizard activation
    Then tap on position "0","0" using adb
      And sleep 3 seconds
      And Fail if the Text "English" not appears on screen

    # At welcome page
    # check the box next to Terms and Conds
    # Then tap on position "60","1242" using adb
    #     And sleep 10 seconds
    #     # press the right arrow button
    #     And tap on button "android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"
    Then tap on position "60","1242" using adb
      And sleep 5 seconds
      And tap on button "android.widget.ImageView":"resource-id":"com.tinklabs.activateapp:id/image_view_begin_btn"
      And sleep 3 seconds


    # Then sleep 10 seconds
    # bypass checkout day currently, i should press the skip button
    Then Wait until "When are you checking out?" appears on screen, timeout "10" seconds
      And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
      And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"
    # Then tap on button with text "SKIP"

    # Then bypass facebook registration currently, i should press the skip button
    Then sleep 1 seconds
      And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
      And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"

    # Then bypass personalize experience registration currently, i should press the skip button
    Then sleep 1 seconds
      And Fail if the resources-id"com.tinklabs.activateapp:id/tv_skip" not appears
      And tap on button "android.widget.TextView":"resource-id":"com.tinklabs.activateapp:id/tv_skip"

    # wait a moment for video to load
    Then sleep 5 seconds
      And Fail if the Video"com.tinklabs.launcher:id/video_view" not appears

    # Let's start should appears
    Then Wait until "Let's Start" appears on screen, timeout "180" seconds
      And Fail if the button "Let's Start" not appears on screen
      And tap on text "Let's Start"

    # TODO: finish
    # Then tap on button "android.widget.TextView":"text":"Let's Start"
    #   And Fail if the activity "com.tinklabs.launcher.features.main.activity.LauncherActivity" not active in "10" seconds

