import can
import time
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
counter = 0
while True:
    msg = can.Message(arbitration_id=0x001,data=[counter],extended_id=False)
    print(counter)
    counter = counter +1
    bus.send(msg)
    time.sleep(1)
