from is_msgs.common_pb2 import Position
from is_wire.core import Channel, Logger, Status, StatusCode
from is_wire.rpc import ServiceProvider, LogInterceptor
from RequisicaoRobo_mensagem.RequisicaoRobo_pb2 import RequisicaoRobo
import time

name = "Controller"
log = Logger(name)

class Robot:
    def __init__(self, id, x=0, y=0, z=0):
        self.id = id
        self.position = Position(x=x, y=y, z=z)

    def set_position(self, x, y, z):
        self.position.x = x
        self.position.y = y
        self.position.z = z

log.info("Inicializando robôs...")
robots = [Robot(id, x=id, y=id, z=0) for id in [1, 2, 3, 4]]
for robot in robots:
    pos = robot.position
    log.info(f"Robô {robot.id}: X: {pos.x} | Y: {pos.y} | Z: {pos.z}")

def get_position(msg, ctx):
    id = msg.id
    reply_to = ctx.reply.topic
    ctx.reply.topic = 'Controle.Console'
    log.info(f"Requisição para pegar a posição do robô {id} feita por {reply_to}.")
    time.sleep(0.5)  # Aguardar meio segundo antes de processar

    try:
        robot = next(r for r in robots if r.id == id)
        pos = robot.position
        log.info(f"Posição do robô {id} encontrada: X: {pos.x} | Y: {pos.y} | Z: {pos.z}")
        log.info(f"Enviando resposta para {reply_to}...")
        time.sleep(0.5)  # Aguardar meio segundo antes de enviar resposta

        response = RequisicaoRobo(id=id, function="get_position")
        response.positions.x = pos.x
        response.positions.y = pos.y
        response.positions.z = pos.z
        return response
    except StopIteration:
        log.error(f"Robô {id} não encontrado. Enviando resposta para {reply_to}.")
        return Status(StatusCode.NOT_FOUND, f"Robô {id} não encontrado.")

def set_position(msg, ctx):
    id = msg.id
    reply_to = ctx.reply.topic
    ctx.reply.topic = 'Controle.Console'
    x, y, z = msg.positions.x, msg.positions.y, msg.positions.z
    log.info(f"Requisição para setar a posição do robô {id} feita por {reply_to}.")
    time.sleep(0.5)  # Aguardar meio segundo antes de processar

    try:
        robot = next(r for r in robots if r.id == id)
        robot.set_position(x, y, z)
        pos = robot.position
        log.info(f"Posição do robô {id} atualizada: X: {pos.x} | Y: {pos.y} | Z: {pos.z}")
        log.info(f"Enviando resposta para {reply_to}...")
        time.sleep(0.5)  # Aguardar meio segundo antes de enviar resposta

        response = RequisicaoRobo(id=id, function="set_position")
        response.positions.x = pos.x
        response.positions.y = pos.y
        response.positions.z = pos.z
        return response
    except StopIteration:
        log.error(f"Robô {id} não encontrado. Enviando resposta para {reply_to}.")
        return Status(StatusCode.NOT_FOUND, f"Robô {id} não encontrado.")
    except Exception as e:
        log.error(f"Erro ao setar a posição do robô {id}: {e}. Enviando resposta para {reply_to}.")
        return Status(StatusCode.INVALID_ARGUMENT, "A posição deve ser um número positivo.")

log.info("Criando canal...")
channel = Channel("amqp://guest:guest@10.10.0.91:5672")

log.info("Criando RPC Server...")
provider = ServiceProvider(channel)
provider.add_interceptor(LogInterceptor())

provider.delegate(
    topic="Controller.get_position",
    function=get_position,
    request_type=RequisicaoRobo,
    reply_type=RequisicaoRobo
)

provider.delegate(
    topic="Controller.set_position",
    function=set_position,
    request_type=RequisicaoRobo,
    reply_type=RequisicaoRobo
)

provider.run()
