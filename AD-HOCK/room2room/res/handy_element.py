# coding:utf-8
import os

pkg = 'com.tinklabs.handyphone'
# Package 相關
Package = {}
Package['appPackage'] = pkg
Package['appActivity'] = pkg + '.features.splash.SplashActivity'
Package['appActivity_M808'] = pkg + '.activities.MainActivity'


# screen lock
lockScreen_byRID = {}
lockScreen_byRID['unlock'] = 'com.tinklabs.launcher:id/item_home_feed_post_item_description_text'


# handy phone tab text in english
handyPhone_tab_byString = {}
handyPhone_tab_byString['phonebook'] = 'PHONE BOOK'
handyPhone_tab_byString['dialler'] = 'DIALLER'

# handy phone book function
handyPhoneBook_function_byString = {}
handyPhoneBook_function_byString['r2r'] = 'Room to Room Call'
handyPhoneBook_function_byString['local'] = 'Local Call'

# handy phone dialler pannel
handyPhoneDialler_pannel_byRID = {}
handyPhoneDialler_pannel_byRID['input'] = pkg + ':id/input_number'
handyPhoneDialler_pannel_byRID['call'] = pkg + ':id/fab'

# android phone dialler pannel
androidDialler_pannel_byRid = {}
androidDialler_pannel_byRid['name'] = "com.android.dialer:id/name"
androidDialler_pannel_byRid['state'] = "com.android.dialer:id/callStateLabel"
androidDialler_pannel_byRid['RoomNumber'] = 'com.android.dialer:id/label'
androidDialler_pannel_byRid['phoneNumber'] = 'com.android.dialer:id/phoneNumber'
androidDialler_pannel_byRid['time'] = 'com.android.dialer:id/elapsedTime'