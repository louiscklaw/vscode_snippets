#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='%s' % __file__.replace('.py', '.log'),
                    filemode='a')

from fabric.api import cd, local, run, task, sudo, settings

PROJ_HOME = os.path.dirname(__file__)
VENV_PATH = 'venv_pyadb'


def feedLocalCommand(commands):
    for command in commands:
        local(command)


def create_adb_command(command_wanted):
    return 'adb %s' % command_wanted


def adb_reboot(state):
    if state in ['bootloader']:
        feedLocalCommand(
            ['adb reboot bootloader']
        )


def fastboot_unlock():
    feedLocalCommand(
        [
            'fastboot -i 0x489 oem fih on',
            'fastboot -i 0x489 oem devlock key'
        ]
    )


def fastboot_reboot():
    feedLocalCommand(
        ['fastboot reboot']
    )


@task
def fastboot_erase_userdata():
    feedLocalCommand(
        [
            create_adb_command('wait-for-device'),
            create_adb_command('reboot bootloader')
        ]
    )

    fastboot_unlock()
    feedLocalCommand(
        ['fastboot -i 0x489 erase userdata']
    )

    fastboot_reboot()


@task
def setup_virtualenv():
    with cd(PROJ_HOME):
        local('python3 -m virtualenv %s' % VENV_PATH)
        local('pip install -r requirements.txt')


@task
def run_test(run_count):
    run_count = int(run_count)
    with settings(warn_only=True):
        for i in range(1, run_count + 2):
            print('run count :%d/%d ' % (i, run_count))
            local('python3 random_click.py')


@task
def activate_venv():
    with cd(PROJ_HOME):
        local('source ./%s/bin/activate' % VENV_PATH)


@task
def mask_udev_android():
    """to provide a method to mask the android uid in linux"""
    with cd('/etc/udev/rules.d'):
        tochange = 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0489", MODE="0666", GROUP="plugdev"'
        sudo('echo %s >> 51-android.rules' % tochange)
