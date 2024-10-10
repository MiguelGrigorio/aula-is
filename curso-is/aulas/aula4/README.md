# is-wire 

## Basic Request/Reply

### Create a RPC Server

O rpc server terá um método chamado "delegate" que  faz um bind de uma função para um particular topic, para que toda vez que um mensagem é
recebida neste topic a função vai ser chamada.

## Run the example

### Executar um amqp broker localmente com o comando abaixo:

```
docker run -d --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.7.6-management
```

### Executar o RPC server, no qual encontra-se [/exemplo](https://github.com/matheusdutra0207/is-wire-RPC/tree/main/exemplo)

```
python3 rpc_server_controle_robot.py
```
Pronto, agora só mandar requests para o rpc. Os exemplos de request encontram-se também em [/exemplo](https://github.com/matheusdutra0207/is-wire-RPC/tree/main/exemplo).

### Get position

```
python3 get_position.py
```

### Set position

```
python3 set_position.py <position x> <position y>
```






