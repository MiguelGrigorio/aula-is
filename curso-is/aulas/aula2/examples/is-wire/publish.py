from is_wire.core import Channel, Message

# Connect to the broker
channel = Channel("amqp://guest:guest@localhost:5672")

message = Message()
message.body = "Hello!".encode('latin1')

while True:
    # Broadcast message to anyone interested (subscribed)
    channel.publish(message, topic="MyTopic.SubTopic")
