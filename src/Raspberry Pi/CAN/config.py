import can
import os
import time


def init_can_bus():
    os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
    time.sleep(0.5)
    return can.interface.Bus(channel='can0', bustype='socketcan_native')


def deinit_can_bus():
    os.system("sudo /sbin/ip link set can0 down")
