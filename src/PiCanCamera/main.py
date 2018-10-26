import os
import time
import can
import numpy as np
from picamera import PiCamera
from cpiclib import CPicLib
from PIL import Image


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
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.5)
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

camera = PiCamera()
camera.resolution = (384, 240)
image_id = 1

my_c_pic_lib = CPicLib()

while True:
    try:
        # Nimmt ein Bild auf und wandelt dieses in ein numpy Array
        image_array = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)
        camera.capture(image_array, 'rgb')

        pil_image = Image.fromarray(image_array).convert('L')

        image_grey_array = np.asarray(pil_image, dtype=np.uint8)
        

        # Das numpy Array wird an die C-Library uebergeben. Dort wird das Bild verarbeitet und es kommt ein
        # Array aus Mittelpunkten dabei heraus
        analyzed_sample_array = my_c_pic_lib.sobel_operator(image_grey_array) # Hier kommt Tobis C Funktion ins Spiel

        points = my_c_pic_lib.resolve_mid(analyzed_sample_array)

        x_points = [int(p[0]) for p in points]

        # Fuer jeden errechneten Mittelpunkt wird eine CAN-Nachricht abgeschickt.
        # Wie die CAN-Nachricht aufgebaut ist, kann in der Funktion nachgelesen werden
        send_messages_for_image_samples(x_points, image_id)
        image_id += 1

        time.sleep(2)

    except Exception as e:
        print(e)
        os.system("sudo /sbin/ip link set can0 down")
        exit()
