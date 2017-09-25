
@adb_command
Feature: adb shell

  @adb_shell
  @test_adb_push_file
  Scenario: adb shell helloworld
    # Given ADB Init session
    Given ADB shell "echo 'helloworld'"
