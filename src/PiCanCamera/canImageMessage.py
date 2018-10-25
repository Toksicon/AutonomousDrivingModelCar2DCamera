import os
import time
import can
import numpy as np
from picamera import PiCamera


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


endian_system = "little"
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.5)
bus = can.interface.Bus(channel='can0', bustype='socket_can_native')

camera = PiCamera()
camera.resolution = (360, 240)
image_id = 1

while True:
    try:
        # Nimmt ein Bild auf und wandelt dieses in ein numpy Array
        image = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)
        camera.capture(image, 'rgb')

        # Das numpy Array wird an die C-Library uebergeben. Dort wird das Bild verarbeitet und es kommt ein
        # Array aus Mittelpunkten dabei heraus
        analyzed_sample_array = clibliblib(image) # Hier kommt Tobis C Funktion ins Spiel

        # Fuer jeden errechneten Mittelpunkt wird eine CAN-Nachricht abgeschickt.
        # Wie die CAN-Nachricht aufgebaut ist, kann in der Funktion nachgelesen werden
        send_messages_for_image_samples(analyzed_sample_array, image_id)
        image_id += 1

        time.sleep(2)

    except Exception as e:
        print(e)
        os.system("sudo /sbin/ip link set can0 down")
        exit()
