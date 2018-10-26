import can
import time


def send_messages_for_image_samples(analyzed_samples, image_id):
    sample_number = 1
    number_of_sample = len(analyzed_samples)

    for sample in analyzed_samples:
        # Aufbau der CAN-Nachricht:
        # 16-Bit ImageID, 8-Bit Anzahl an Samples, 8-Bit aktuell erhaltene Sample-Nummer, 32-Bit Nutzdaten

        payload = bytearray()

        payload.extend(image_id.to_bytes(2, endian_system))
        payload.extend(number_of_sample.to_bytes(1, endian_system))
        payload.extend(sample_number.to_bytes(1, endian_system))
        payload.extend(sample.to_bytes(4, endian_system))

        message = can.Message(is_remote_frame=False, extended_id=False, arbitration_id=0x200,
                              dlc=len(payload), data=payload)
        bus.send(message)

        sample_number += 1
        time.sleep(1)


endian_system = "little"
