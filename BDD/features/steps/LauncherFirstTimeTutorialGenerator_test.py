#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.INFO)

from LauncherFirstTimeTutorialGenerator import *

tutorial_config = LauncherFirstTimeTutorialConfig('en_US')
tutorial_route = LauncherFirstTimeTutorialGenerator(tutorial_config, 'T1')
logging.debug(tutorial_route.get_tutorial())
