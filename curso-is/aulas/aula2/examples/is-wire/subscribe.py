from __future__ import print_function
from is_wire.core import Channel, Subscription
import time

# Connect to the broker
channel = Channel("amqp://guest:guest@localhost:5672")

# Subscribe to the desired topic(s)
subscription = Subscription(channel)
subscription.subscribe(topic="MyTopic.SubTopic")
# ... subscription.subscribe(topic="Other.Topic")

while True:
    message = channel.consume()
    print(message.body.decode('latin1'))
    time.sleep(1)
