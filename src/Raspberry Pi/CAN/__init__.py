import can
import time
import os


class Can:
    def __init__(self, endian_system="little"):
        self._endian_system = endian_system

    def __enter__(self):
        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
        time.sleep(0.5)
        self._bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.system("sudo /sbin/ip link set can0 down")

    def send_messages_for_image_samples(self, analyzed_samples, image_id):
        sample_number = 1
        number_of_sample = len(analyzed_samples)

        for sample in analyzed_samples:
            # Aufbau der CAN-Nachricht:
            # 16-Bit ImageID, 8-Bit Anzahl an Samples, 8-Bit aktuell erhaltene Sample-Nummer, 32-Bit Nutzdaten

            payload = bytearray()

            payload.extend(image_id.to_bytes(2, self._endian_system))
            payload.extend(number_of_sample.to_bytes(1, self._endian_system))
            payload.extend(sample_number.to_bytes(1, self._endian_system))
            payload.extend(sample.to_bytes(4, self._endian_system))

            message = can.Message(is_remote_frame=False, extended_id=False, arbitration_id=0x200,
                                  dlc=len(payload), data=payload)
            self._bus.send(message)

            sample_number += 1
            time.sleep(1)

