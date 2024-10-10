from __future__ import print_function
from is_wire.core import Channel, Message, Subscription, Logger
from google.protobuf.empty_pb2 import Empty
import socket
from is_msgs.common_pb2 import Position

# Programa para fazer o "get position"

log = Logger(name='get_position')

empty = Empty()

channel = Channel("amqp://guest:guest@localhost:5672")
subscription = Subscription(channel)
request = Message(content=empty, reply_to=subscription)
channel.publish(request, topic="Get.Position")

try:
    reply = channel.consume(timeout=1.0)
    position = reply.unpack(Position)
    log.info(f'x = {position.x}, y = {position.y}')

except socket.timeout:
    print('No reply :(')