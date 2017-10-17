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
                    filename='debug.log',
                    filemode='a')

from fabric.api import cd, run, local, env
from datetime import datetime

def get_today_string():
    return datetime.now().strftime('%d%m%Y-%H%M%S')


class FabricException(Exception):
    pass


APPIUM_BINARY = r'/usr/local/bin/appium'

def create_appium_process(port, bootstrapport, android_serial):
    """
    create appium process, provided that the listening port, bootstrap port and android serial to catch.abs

    Args:
        port: appium listening port
        bootstrapport: TODO: fill me up, the appium's bootstrap port
        android_serial: android_serial number udid

    TODO: background run this process.
    """
    local(APPIUM_BINARY + '-p %s  -bp %s  -s %s' %
          (port, bootstrapport, android_serial))


def destroy_appium_process(android_serial):
    """
    to kill the appium process identified by it's android_serial

    Args:
        android_serial: android serial number udid
    """
    appium_pid_by_serial = local("ps -axl|grep -i %s|grep -i appium |awk '{print $2}'" % android_serial)
    local('kill %s' % appium_pid_by_serial)


def run_test(command):
    # NOTE: behave random-click-1-hour_selftest.feature --tags=test_swipe_feed_trending -vk
    log_file_filename = get_today_string() + '.out'
    local('%s |tee %s' % (command, log_file_filename))


def run_test_M812_selftest():
    # NOTE: test procedure for M812
    logging.error('for T1 only')
    # run_test('behave  random-click-1-hour_selftest.feature')
    pass


def run_test_VZH_selftest():
    # NOTE: test procedure for VZH
    run_test('behave  random-click-1-hour_selftest.feature')
    pass

def run_llaw_localtest(tags,number_of_run):
    """
    to launch the test

    Args:
        tags: tags of behave test script
        number_of_run: the times of test should be executed

    EXAMPLE:
        fab run_llaw_localtest:test_quick_selftest,1
        fab run_llaw_localtest:integrate,1
    """
    env.abort_exception = FabricException

    logging.debug('for llaw self test on local machine')
    number_of_run = int(number_of_run)

    for run in range(1,number_of_run+1):
        logging.debug('running %d of %d ...' % (run, number_of_run))

        log_file_filename = get_today_string() +'.out'

        try:
            logging.debug(
                local(
                    'behave random-click-1-hour_selftest.feature --tags=%s -vk | tee ./result/%s' % (tags, log_file_filename))
                )
            pass
        except FabricException:
            logging.debug('ignore exception')
            # NOTE: ignore exception
            pass
        else:
            pass


def helloworld():
    local('echo helloworld')
    logging.debug('filename: %s' % __file__)
