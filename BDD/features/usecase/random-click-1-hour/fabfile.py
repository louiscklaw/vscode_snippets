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
                    'behave random-click-1-hour_selftest.feature --tags=%s -vk | tee ./result/%s.out' % (tags, log_file_filename))
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
