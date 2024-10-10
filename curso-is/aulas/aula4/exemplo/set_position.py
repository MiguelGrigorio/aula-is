from __future__ import print_function
from is_wire.core import Channel, Message, Subscription, Logger, Status
import socket
from is_msgs.common_pb2 import Position
import sys

log = Logger(name='set_position')

# Programa para fazer o "set position"

# valores pegos ao chamar o programa
x = int(sys.argv[1])
y = int(sys.argv[2])
postion = Position(x=x, y=y) 

channel = Channel("amqp://guest:guest@localhost:5672")
subscription = Subscription(channel)
request = Message(content=postion, reply_to=subscription)
channel.publish(request, topic="Set.Position")

try:
    reply = channel.consume(timeout=1.0)
    log.info(f'{reply.status.code}')
    
except socket.timeout:
    print('No reply :(')