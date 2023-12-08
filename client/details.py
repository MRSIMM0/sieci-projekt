import psutil
import json
import os
import socket

class Details():
    def __init__(self):
        self.name = socket.gethostname()
        self.osName = os.name
        self.cpu = psutil.cpu_percent(4)
        self.ramUsed = "{:.1f}".format(psutil.virtual_memory()[3]/1000000000)
        self.ramTotal = "{:.1f}".format(psutil.virtual_memory()[0]/1000000000)
        self.ramPercentage = round(float(self.ramUsed) / float(self.ramTotal) * 100, 2)
        disk = psutil.disk_usage('/')
        self.diskTotal = "{:.1f}".format(disk.total/1000000000)
        self.diskUsed = "{:.1f}".format(disk.used/1000000000)
        self.diskFree = "{:.1f}".format(disk.free/1000000000)
        self.diskPercentage = disk.percent

    def getJson(self):
        return json.dumps(self.__dict__)