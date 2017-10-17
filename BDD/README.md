# BDD for handy app on android platform

### What is this repository for?
* perform test by BDD way
### How do I get set up?
* MAC:
    python >=2.7.10
    node >= 8.4.0
    appium = 1.6.5
    adb = 1.0.39
    fastboot = 3db08f2c6889-android

* python
    `pip install -r requirements.txt`

# to start the appium for the test
1. connect to the device by USB
1. enable the ADB on device, if the reset/reboot is required during the test. a "ADB always enabled" ROM is required.
1. start a appium session, seperated by the android_serial(udid)
    * `appium -p 4725 -bp 4726 -U V2HGLMB721301100`
1. start the test,
    * `behave -vk <path_to_the_feature_file>`

# branch definitation
* feature/random-click-1-hour
    * working branch for random-click-1-hour development


#TODO:
[ ] - merge the branch M812 back to the MAIN BDD branchg
