#!/usr/bin/env python
# coding:utf-8
import os, sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG,
   format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
   datefmt='%a, %d %b %Y %H:%M:%S',
   filename='debug.log',
   filemode='a')

from datetime import datetime

def screen_capture(context, sTargetPath):
    """simple facility to provide screen capture
        TODO: generalize me
    """

    try:
        # adb shell screencap -p /sdcard/$sc.png
        # try:
        dParameter = {}
        dParameter['sEpoch'] = datetime.now().strftime('%s')
        dParameter['sTargetPath'] = sTargetPath
        dParameter['sTargetPathWithDatetime'] = os.path.join(
            dParameter['sTargetPath'], dParameter['sEpoch'])

        lsADBCommand = []
        lsADBCommand.append(
            'shell screencap -p /sdcard/%(sEpoch)s.png' % dParameter)
        lsADBCommand.append(
            'pull /sdcard/%(sEpoch)s.png %(sTargetPathWithDatetime)s' % dParameter)
        lsADBCommand.append('shell rm /sdcard/%(sEpoch)s.png' % dParameter)
        lsADBCommand.append('shell uiautomator dump')
        lsADBCommand.append(
            'pull /sdcard/window_dump.xml %(sTargetPathWithDatetime)s/dump.uix' % dParameter)
        lsADBCommand.append('shell rm /sdcard/window_dump.xml' % dParameter)

        # NOTE create a landing directory for screen capture
        os.makedirs(dParameter['sTargetPathWithDatetime'], 0755)

        adb = context.ADBSession
        for sADBCommand in lsADBCommand:
            adb.run_cmd(sADBCommand)
    except Exception:

        # TODO: remove me
        from pprint import pprint
        print('dump the value of: sTargetPath')
        pprint(sTargetPath)

        print('dump the value of: dParameter')
        pprint(dParameter)
        # TODO: remove me

    pass

