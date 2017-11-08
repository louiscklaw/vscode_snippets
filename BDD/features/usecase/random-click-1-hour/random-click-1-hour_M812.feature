
Feature: random click for a hour, pilot run
  @initialize_rom
  Scenario: initialize
    Given Target device is M812 "PHXGLC1582600007"
    Given adb binary is available
    Given appium is running

    Given Fastboot init
    Given FASTBOOT Erase userdata
    And ADB Wait for device, timeout 600 seconds

    # about 600 for T1
    # about 900 for M812
    And ADB check boot completed, timeout 900 seconds

    # Then Wait for handy initialization
    Then sleep 60 seconds

    Given ADB PATH_ANDROID_TEMP directory is ready, timeout 60 seconds
      And ADB push tinklabs1001

    Then ADB change permission tinklabs1001

    Then ADB settings put global package_verifier_enable 0

    # Given setup an android as below, using appium port 4725
    #   | Package                  | Activity                        | platform | type  | version |
    #   | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    # And Wait until "English" appears on screen, timeout "600" seconds

    # Given Reach "Happy flow The end" page in WizardActivity by skip, route "THIS_TEXT_IS_RESERVED_FOR_LATTER_USE"
    # And Skip the 1st time tutorial by launcher

    # disable swipe random route
    # Then Random tour for 0.5 hour


    # Then In launcher side menu, Erase data
    # # unconditional wait due to loss connection to the phone
    # And sleep 180 seconds

    # Then ADB Wait for device
    # And ADB check boot completed, timeout 600 seconds
    # Then Wait for handy initialization
    # And ADB Initialize android
    # And setup an android as below, using appium port 4725
    #   | Package                  | Activity                        | platform | type  | version |
    #   | com.tinklabs.activateapp | .features.wizard.WizardActivity | Android  | phone | 7.0     |
    # And Wait until "English" appears on screen, timeout "600" seconds
