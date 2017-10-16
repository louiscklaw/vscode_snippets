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

from fabric.api import cd, run, local
from datetime import datetime
today = datetime.now().strftime('%d%m%Y-%H%M%S')


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


def helloworld():
    local('echo helloworld')
    print('filename: %s' % __file__)
