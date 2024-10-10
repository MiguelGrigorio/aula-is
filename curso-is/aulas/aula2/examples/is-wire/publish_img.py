from is_wire.core import Channel, Subscription, Message
from is_msgs.image_pb2 import Image
import cv2
import numpy as np
import time


def to_image(input_image, encode_format='.jpeg', compression_level=0.8):
    if isinstance(input_image, np.ndarray):
        if encode_format == '.jpeg':
            params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
        elif encode_format == '.png':
            params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format, img=input_image, params=params)
        return Image(data=cimage[1].tobytes())
    elif isinstance(input_image, Image):
        return input_image
    else:
        return Image()

channel = Channel('amqp://guest:guest@localhost:5672')

img = cv2.imread("./cars.jpg")

img_message = Message()
img_message.pack(to_image(img))

while True:
    channel.publish(img_message, topic='Topic.Frame')
    time.sleep(1)