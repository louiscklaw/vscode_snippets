
nohup adb shell screenrecord  /sdcard/test.mp4 &

behave -vk random-click-1-hour_selftest.feature  --tags=wip

adb pull /sdcard/test.mp4 .