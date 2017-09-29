import utils

class DevicesInfo:
    def __init__(self,device):
        self.device = device
    def getManufacturer(self):
        cmd = 'adb -s ' + self.device + ' shell getprop ro.product.manufacturer'
        return utils.osCommand(cmd)

    def getModel(self):
        cmd = 'adb -s ' + self.device + ' shell getprop ro.product.model'
        return utils.osCommand(cmd)

    def getBrand(self):
        cmd = 'adb -s ' + self.device + ' shell getprop ro.product.brand'
        return utils.osCommand(cmd)

    def getAndroidVersion(self):
        cmd = 'adb -s ' + self.device + ' shell getprop ro.build.version.release'
        return utils.osCommand(cmd)

    def getSDKVersion(self):
        cmd = 'adb -s ' + self.device + ' shell getprop ro.build.version.sdk'
        return utils.osCommand(cmd)

    def getSerialNo(self):
        cmd = 'adb -s ' + self.device + ' shell getprop ro.serialno'
        return utils.osCommand(cmd)
