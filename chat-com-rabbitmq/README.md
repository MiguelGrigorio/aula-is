# Chat com RabbitMQ

Nessa aula a ideia era com que utilizasse a biblioteca is-wire em conjunto com RabbitMQ para enviar e receber mensagens simulando um chat de conversa.

Para critério de customização, cada código tem um arquivo de configuração .env que contém o IP do broker que deseja conectar.

<h2>Publish</h2>

No arquivo [pub.py][1], é onde o código pega a mensagem e envia para o canal no tópico desejado.

Primeiramente foi conectado ao broker do espaço inteligente, que é o RabbitMQ.

```py
# Conectando ao broker
channel = Channel(f"amqp://guest:guest@{ip}")
```
Logo após tem a construção da mensagem, definição do remetente, tópico e destinatário.
```py
# Cria a mensagem
message = Message()

# Define quem enviou a mensagem
message.reply_to = input("Digite seu nome: ")

# Define o tópico
topico = input("Digite o tópico que deseja enviar: ")

# Define qual a mensagem e o destinatário
mensagem = input("Digite sua mensagem: ")
dest = input("Digite seu destino: ")

# Codifica a mensagem
message.body = mensagem.encode("utf-8")
```

Após isso, depois de todas as informações, o código publica a mensagem no tópico definido.
```py
# Envia a mensagem para o destinatário do tópico
channel.publish(message, topic = f"{topico}.{dest}")
```

<h2>Subscribe</h2>

No arquivo [sub.py][2], é onde consome o canal e filtra apenas para o tópico que deseja.

Funciona semelhantemente ao [pub.py][1], entretanto, o código basicamente fica "ouvindo" ao tópico desejado.

```py
# Subscreve para o tópico
sub.subscribe(topic = f"{topico}.{dest}")
```

E depois, o código recebe as mensagens do canal, e então printa o que foi recebido.

```py
# Recebe a mensagem
message = channel.consume()
print(message.reply_to + ": " + message.body.decode("utf-8"))
```
<h2>Dockerfiles</h2>
Cada pasta tem seu arquivo Dockerfile para conteinerizar esses dois códigos e funcionar separadamente no espaço inteligente.

[1]: pub/pub.py
[2]: sub/sub.py