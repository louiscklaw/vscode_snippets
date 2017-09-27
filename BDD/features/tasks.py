#!/usr/bin/env python

from invoke import run, task

lsCmd=[]
lsCmd.append("pip install -r requirements.txt")
lsCmd.append('behave -vk ./random-click-1-hour.feature')

def list_command_runner(commands):
    for command in commands:
        run(command, hide=False,warn=True)

@task
def screen_recording(context):
    """
        screen recording task
        TODO: implement
    """
    command= r'python screenrecord.py 180 /home/louislaw/_workspace/handy-qa-automation/BDD/features/usecase/random-click-1-hour/screenrecord'

    run(command, hide=False, warn=True)

    pass


@task
def archive_screen_capture(context):
    """
        task to archive screen capture
        TODO: implement
    """
    commands=[]
    for i in range(1,10+1):
        for command in commands:
            result = run(command, hide=False, warn=True)
            print(result.ok)

@task
def archive_screen_recording(context):
    """
        task to archive screen recording
        TODO: implement
    """
    pass

@task
def simple_task(context):
    """
        a dummy task for louis
    """
    print('hi -> bye')
    pass


@task
def fastboot_clear(context):
    """
        task to handle fastboot erase
        TODO: add adb reboot bootloader by threading
    """
    commands=[]
    commands.append('fastboot -i 0x489 oem fih on')
    commands.append('fastboot -i 0x489 oem devlock key')
    commands.append('fastboot -i 0x489 erase userdata')
    commands.append('fastboot -i 0x489 erase oem')
    commands.append('fastboot -i 0x489 erase logdump')

    list_command_runner(commands)

    pass

@task
def fastboot_reboot(context):
    """
        task to handle fastboot reboot
    """
    commands=[]
    commands.append('fastboot -i 0x489 reboot')

    list_command_runner(commands)

    pass

@task
def download_fastboot(context):
    """
        task to handle fastboot download
        TODO: implement
    """
    pass


@task
def test_adb_screencap(context):
    """
        to run the test_adb_screen_capture
        TODO: generalize me
    """
    command= 'behave -vk --tags=test_adb_screen_capture .'
    # command= r'echo -n 1'
    result = run(command, hide=False, warn=True)
    # print('helloworld')


@task
def behave_test_listing(context):
    """
        to list out the testtag available from behave
    """
    command = 'behave '
    run(command, hide=False, warn=True)
    pass

@task
def test_rom_sanity(context):
    """
        rom sanity test runner
    """
    for i in range(1, 5+1):
        command= 'behave -vk --tags=test_rom_sanity .'
        run(command, hide=False, warn=True)

@task
def test_random_click_for_an_hour(context):
    """
        to run the random test click
    """
    for i in range(1,999+1):
        command= 'behave -vk --tags=test_random_click_for_an_hour .'
        # command= r'echo -n 1'
        result = run(command, hide=False, warn=True)
        # print('helloworld')
