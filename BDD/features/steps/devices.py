#!/usr/bin/env python


class BasicDeviceConfig():
    # default configuration, based on T1
    DUMMY_TAP = (0, 1201)

    # for the very beginning checkbox
    GREETING_TAC_CHECKBOX = (60, 1242)
    pass


class Device_T1(BasicDeviceConfig):
    DUMMY_TAP = (0, 1201)
    pass


class Device_M812(BasicDeviceConfig):
    GREETING_TAC_CHECKBOX = (71, 1856)

    DUMMY_TAP = (0, 1921)
    pass
