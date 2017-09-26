from behave import given, when, then, step
import os
import sys

# https://github.com/appium/python-client
from appium import webdriver
import android_capabilities

sys.path.append(os.path.dirname(__file__)+'/../_lib')
from android_function import finger

def PATH(p): return os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
