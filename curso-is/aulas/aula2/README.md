# is-wire
- [Laboratório de Visão Computacional e Robótica - LabVISIO](https://github.com/labviros)
- [is-wire](https://github.com/labviros/is-wire-py)

## Publish

### Connect to the broker

```
channel = Channel("amqp://guest:guest@localhost:5672")
```
A variável channel inicializa uma conexão amqp no endereço da url passada e declara uma exchange("is") do tipo “topic”.

### Broadcast message to anyone interested (subscribed)
```
channel.publish(message, topic="MyTopic.SubTopic")
```
O método “publish” irá publicar uma mensagem no tópico informado, ou seja, o mesmo se encarrega de de criar um “amqp.Message” e mandar a mensagem para a exchange "is" com a routing key informada.

## Sub

### Connect to the broker
```
channel = Channel("amqp://guest:guest@localhost:5672")
```

### Subscribe to the desired topic(s)
```
subscription = Subscription(channel)
```
Resumidamente falando, o objeto “subscription” e inicializado com uma função que cria uma fila.
```
subscription.subscribe(topic="MyTopic.SubTopic")
```
Acima, no método "subscribe",  faz-se  o processo de bind da fila com a exchange "is". Desse modo, tudo que for publicado na exchange "is" no tópico “MyTopic.SubTopic”  será encaminhado para essa fila.

### Blocks forever waiting for one message from any subscription
```
message = channel.consume()
print(message)
```

## Run the exemple

### Executar um amqp broker localmente com o comando abaixo:
```
docker run -d --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.7.6-management
```

### Executar o publish

```
from is_wire.core import Channel, Message

# Connect to the broker
channel = Channel("amqp://guest:guest@localhost:5672")

message = Message()
message.body = "Hello!".encode('latin1')

while True:
    # Broadcast message to anyone interested (subscribed)
    channel.publish(message, topic="MyTopic.SubTopic")
```

### Executar um sub para consumir as mensagens

```
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
```
