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
from time import sleep


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
    """
    behave test runner

    Args:
        command: command to run using behave (including behave).

    """
    # NOTE: behave random-click-1-hour_selftest.feature --tags=test_swipe_feed_trending -vk
    log_file_filename = get_today_string() + '.out'
    local('%s |tee %s' % (command, log_file_filename))

def run_command(command):
    """
    run the test without log file

    Args:
        command: command to be executed
    """
    logging.debug('starting running of command %s' % command)
    local('%s' % command)

    logging.debug('clear done')


def run_test_M812_selftest():
    # NOTE: test procedure for M812
    logging.error('for T1 only')
    # run_test('behave  random-click-1-hour_selftest.feature')
    pass


def run_test_VZH_selftest():
    # NOTE: test procedure for VZH
    run_test('behave  random-click-1-hour_selftest.feature')
    pass

def setup_daily_log(base_path, base_filename):
    """
    procedure to setup log file(daily log)

    Args:
        base_path: the path to collect the log file

    """
    daily_log_endstring = get_today_string() + '.log'
    daily_log_filename = base_filename.replace(
        ".", '_') + '_' + daily_log_endstring

    logging.basicConfig(level=logging.DEBUG,
                        filename=base_path + daily_log_filename,
                        filemode='a')


def construct_beahve_command(feature_file_name, feature_result_filename='', tags=''):
    """
    procedure to create behave command

    Args:
        feature_file_name: the feature file want to execute
        tags: the tags wanted, default to 'no-tags'
            '' - no tag
            tag1 - single tag
            tag1,tag2,tag3... = multitag example 1
            tag1,-tag2,tag3... = multitag example 2


    """
    behave_command = ''
    result_parameter = ''

    if tags == '':
        behave_command = 'behave %s' % feature_file_name
        pass

    else:
        # NOTE: defined tags, construct tags parameters
        # NOTE: normanize tags by ,

        # TODO: inprogress
        pass

    if feature_result_filename == '':
        pass
    else:
        logging.debug('feature_result_filename:%s' % feature_result_filename)
        result_parameter = ' | tee %s' % feature_result_filename
        behave_command += result_parameter


    return behave_command


def run_never_end_test(feature_file_name, result_collect_directory, beahve_tags=''):
    """
    keep running of the test

    Args:
        feature_file_name: the .feature file want to execute
        result_collect_directory: result collection directory
        behave_tags: the tags wanted

    Doc:
        http://docs.fabfile.org/en/1.13/usage/fab.html -> Per-task arguments

    NOTE: Example
        fab run_never_end_test:random-click-1-hour_quick_T1.feature,./result/T1
        fab run_never_end_test:random-click-1-hour_quick_M812.feature,./result/M812

    """

    while 1:
        sleep(1)
        logging.debug('result_collect_directory:%s' % result_collect_directory)
        log_file_filename = result_collect_directory + '/' + get_today_string() + '.out'


        behave_execution_log_path = './behave_log/'
        setup_daily_log(behave_execution_log_path, feature_file_name)

        logging.error('feature_file_name:%s' % feature_file_name)

        try:
            print('start')
            print('logfilename: %s' % log_file_filename)
            logging.debug('start run the feature file: %s :' % feature_file_name)
            # logging.debug(
            #     run_command('behave %s | tee ./result/%s' % (feature_file_name, log_file_filename))
            # )
            # local('fastboot reboot')
            logging.debug(
                run_command(
                    construct_beahve_command(
                        feature_file_name, log_file_filename, '')
                    )
            )

        except FabricException as e:
            logging.debug('ignore exception from Fabric')

        except KeyboardInterrupt as e:
            logging.debug('ctrl-c end')
            print('receive ctrl-c, end myself')
            raise e

        else:
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
