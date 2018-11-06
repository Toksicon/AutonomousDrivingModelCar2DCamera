import time
import os

try:
    import can
except:
    can = None
    print('Failed to load can module')


''' EmptyCanMessenger is used, when the can module couldn't be loaded.
    This should only happen in test environments (desktop machines).
'''
class EmptyCanMessenger:
    def __init__(self, can):
        self._can = can

    def send_messages_for_image_samples(self, analyzed_samples, image_id):
        pass


''' CanMessenger implementation is used, when the can module has been loaded.
'''
class CanMessenger(EmptyCanMessenger):
    def __init__(self, can):
        self._can = can

    def send_messages_for_image_samples(self, analyzed_samples, image_id):
        sample_number = 1
        number_of_sample = len(analyzed_samples)

        for sample in analyzed_samples:
            # Aufbau der CAN-Nachricht:
            # 16-Bit ImageID, 8-Bit Anzahl an Samples, 8-Bit aktuell erhaltene Sample-Nummer, 32-Bit Nutzdaten

            payload = bytearray()

            payload.extend(image_id.to_bytes(2, self._can._endian_system))
            payload.extend(number_of_sample.to_bytes(1, self._can._endian_system))
            payload.extend(sample_number.to_bytes(1, self._can._endian_system))
            payload.extend(int(sample[0] * (2 ** 16)).to_bytes(2, self._can._endian_system))
            payload.extend(int(sample[1] * (2 ** 16)).to_bytes(2, self._can._endian_system))

            message = can.Message(is_remote_frame=False, extended_id=False, arbitration_id=0x200,
                                dlc=len(payload), data=payload)
            self._can._bus.send(message)

            sample_number += 1
            time.sleep(0.01)


class Can:
    def __init__(self, endian_system="little"):
        self._endian_system = endian_system

    def __enter__(self):
        if can:
            os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
            time.sleep(0.5)
            self._bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
            return CanMessenger(self)

        # return a dummy can messenger,
        # as the can library couldn't be loaded
        return EmptyCanMessenger(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if can:
            os.system("sudo /sbin/ip link set can0 down")

