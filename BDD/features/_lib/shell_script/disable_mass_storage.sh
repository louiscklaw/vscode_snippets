#!/system/bin/sh

/data/local/tmp/tinklabs1001

/system/bin/getprop |grep -i  persist.sys.usb.config
/system/bin/setprop persist.sys.usb.config mtp,adb,123

/system/bin/getprop |grep -i  persist.sys.usb.config

reboot
