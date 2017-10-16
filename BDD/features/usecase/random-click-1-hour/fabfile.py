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
today = datetime.now().strftime('%d%m%Y-%H%M%S')


class FabricException(Exception):
    pass

def run_test(command):
    # NOTE: behave random-click-1-hour_selftest.feature --tags=test_swipe_feed_trending -vk
    log_file_filename = today + '.out'
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

def run_llaw_localtest(number_of_run):
    env.abort_exception = FabricException

    logging.debug('for llaw self test on local machine')
    number_of_run = int(number_of_run)

    for run in range(1,number_of_run+1):
        logging.debug('running %d of %d ...' % (run, number_of_run))

        try:
            logging.debug(local('behave random-click-1-hour_selftest.feature --tags=test_quick_selftest -vk'))
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
