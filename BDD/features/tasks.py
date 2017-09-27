#!/usr/bin/env python

from invoke import run, task

lsCmd=[]
lsCmd.append("pip install -r requirements.txt")
lsCmd.append('behave -vk ./random-click-1-hour.feature')

def lsCommandRunner(lsCommand):
    for sCommand in lsCommand:
        run(sCommand, hide=False,warn=True)

@task
def screen_recording(context):
    sCmd = r'python screenrecord.py 180 /home/louislaw/_workspace/handy-qa-automation/BDD/features/usecase/random-click-1-hour/screenrecord'
    pass


@task
def archive_screencapture(context):
    for i in range(1,10+1):
        for sCmd in lsCmd:
            result = run(sCmd, hide=False, warn=True)
            print(result.ok)

@task
def archive_screenrecording(context):
    pass

@task
def simple_task(context):
    pass


@task
def fastboot_clear(context):
    lsCommand=[]
    lsCommand.append('fastboot -i 0x489 oem fih on')
    lsCommand.append('fastboot -i 0x489 oem devlock key')
    lsCommand.append('fastboot -i 0x489 erase userdata')
    lsCommand.append('fastboot -i 0x489 erase oem')
    lsCommand.append('fastboot -i 0x489 erase logdump')

    lsCommandRunner(lsCommand)

    pass

@task
def fastboot_reboot(context):
    lsCommand=[]
    lsCommand.append('fastboot -i 0x489 reboot')

    lsCommandRunner(lsCommand)

    pass

@task
def download_fastboot(context):
    pass

@task
def test_adb_screencap(context):
    sCmd = 'behave -vk --tags=test_adb_screen_capture .'
    # sCmd = r'echo -n 1'
    result = run(sCmd, hide=False, warn=True)
    # print('helloworld')

@task
def test_rom_sanity(context):
    """
        rom sanity test runner
    """
    for i in range(1, 5+1):
        sCmd = 'behave -vk --tags=test_rom_sanity .'
        run(sCmd, hide=False, warn=True)

@task
def test_random_click_for_an_hour(context):
    sCmd = 'behave -vk --tags=test_random_click_for_an_hour .'
    # sCmd = r'echo -n 1'
    result = run(sCmd, hide=False, warn=True)
    # print('helloworld')
