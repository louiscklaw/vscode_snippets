Feature: adb shell

  @sanity
  Scenario: adb shell helloworld
    # Given ADB Init session
    Given ADB shell "echo 'helloworld'"

  @wip
  Scenario: test checking android temporary directory
    Given ADB PATH_ANDROID_TEMP directory is ready, timeout 60 seconds

