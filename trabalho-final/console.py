from is_wire.core import Channel, Logger, Message, Status, StatusCode, Subscription
from is_wire.rpc import ServiceProvider, LogInterceptor
from RequisicaoRobo_mensagem.RequisicaoRobo_pb2 import RequisicaoRobo
import socket
import random
import time

name = "Console"
log = Logger(name)
system = 'Off'

log.info("Criando canal...")
channel = Channel("amqp://guest:guest@10.10.0.91:5672")
subscription = Subscription(channel)
subscription.subscribe(f"Controle.{name}")

def turn_on():
    time.sleep(1)
    return random.choice(["On", "Off"])

def send_message(content, dest):
    message = Message(reply_to=name, content=content.encode("utf-8"))
    channel.publish(message, topic=f'Controle.{dest}')
    
def request_robot(msg, ctx):
    function = msg.function
    id = msg.id
    reply_to = ctx.reply.topic
    ctx.reply.topic = 'Controle.Operator'
    
    if function not in ["get_position", "set_position"]:
        log.error(f"Função ({function}) inválida.")
        return Status(StatusCode.INVALID_ARGUMENT, f"Função ({function}) inválida.")

    topic_action = "Controller.get_position" if function == "get_position" else "Controller.set_position"
    log.info(f"Requisição para {'pegar' if function == 'get_position' else 'setar'} a posição do robô {id} feita por {reply_to}...")
    
    channel.publish(Message(content=msg, reply_to=name), topic=topic_action)
    attempts = 0
    while True:
        try:
            message = channel.consume(timeout=4.0)
            if message.status.code == StatusCode.OK:
                message = message.unpack(RequisicaoRobo)
                log.info(f"ID: {message.id} / Função: {message.function} / Posição do robô {id}: X: {message.positions.x} | Y: {message.positions.y} | Z: {message.positions.z}")
                log.info(f"Enviando resposta para {reply_to}...")
                time.sleep(1)
                return message
            else:
                log.error(message.status.why)
                log.error(f"Enviando resposta para {reply_to}.")
                return Status(StatusCode.NOT_FOUND, f"Robô {id} não encontrado.")
        except socket.timeout:
            if attempts >= 3:
                log.error("Número máximo de tentativas atingido.")
                return Status(StatusCode.DEADLINE_EXCEEDED, "Número máximo de tentativas atingido.")
            attempts += 1
            log.warn("Timeout. Tentando novamente...")
            time.sleep(1)

while system == 'Off':
    log.info("Esperando mensagem para ligar...")
    message = channel.consume()
    msg = message.body.decode("utf-8")
    dest = message.reply_to

    if msg != "Ligar sistema":
        continue

    log.info("Mensagem recebida. Tentando ligar o sistema...")
    system = turn_on()
    log.info("Sucesso ao ligar o sistema.") if system == 'On' else log.warn("Falha ao ligar o sistema.")
    log.info(f"Enviando resposta para {dest}...")
    send_message(system, dest)

log.info("Criando RPC Server...")
provider = ServiceProvider(channel)
provider.add_interceptor(LogInterceptor())

provider.delegate(
    topic="Requisicao.Robo",
    function=request_robot,
    request_type=RequisicaoRobo,
    reply_type=RequisicaoRobo
)

provider.run()