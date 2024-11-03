from is_wire.core import Channel, Logger, Message, StatusCode, Subscription
from RequisicaoRobo_mensagem.RequisicaoRobo_pb2 import RequisicaoRobo
from random import randint
import time

system = 'Off'
name = "Operator"
log = Logger(name)

log.info("Criando canal...")
channel = Channel("amqp://guest:guest@10.10.0.91:5672")
subscription = Subscription(channel)
subscription.subscribe(f"Controle.{name}")

def choosing_robot(function, id, x=None, y=None, z=None):
    if function not in ["get_position", "set_position"]:
        log.error(f"Função ({function}) inválida.")
        return SyntaxError

    log.info(f"Robô escolhido: {id}")

    robot = RequisicaoRobo()
    robot.id = id
    robot.function = function

    if function == "get_position":
        log.info("Criando mensagem para pegar a posição...")
        channel.publish(Message(content=robot, reply_to=name), topic="Requisicao.Robo")
    else:
        log.info("Criando mensagem para setar a posição...")
        robot.positions.x = x if x is not None else randint(1, 5)
        robot.positions.y = y if y is not None else randint(1, 5)
        robot.positions.z = z if z is not None else randint(1, 5)
        log.info(f"Tentativa | Robô ID: {id} / Posição: X: {robot.positions.x} | Y: {robot.positions.y} | Z: {robot.positions.z}")
        channel.publish(Message(content=robot, reply_to=name), topic="Requisicao.Robo")

    log.info("Esperando resposta...")
    attempts = 0
    while True:
        try:
            msg = channel.consume(timeout=2.0)
            if msg.status.code == StatusCode.OK:
                message = msg.unpack(RequisicaoRobo)
                position = message.positions
                if function == "get_position":
                    log.info(f"Robô ID: {id} / Função: {function} / Posição: X: {position.x} | Y: {position.y} | Z: {position.z}")
                    break
                else:
                    log.info(f"Robô ID: {id} / Função: {function} / Status: {msg.status.code}")
                    break
            else:
                log.error(msg.status.why)
        except TimeoutError:
            if attempts >= 3:
                log.error("Número máximo de tentativas atingido.")
                break
            attempts += 1
            log.warn("Timeout. Tentando novamente...")
            time.sleep(1)  # Aguardar antes de tentar novamente

def turn_on():
    global system

    log.info("Criando mensagem para ligar...")
    message_turn_on = Message()
    message_turn_on.reply_to = name
    message_turn_on.body = "Ligar sistema".encode("utf-8")
    attempts = 0
    while system == 'Off':
        log.info("Enviando mensagem para ligar...")
        channel.publish(message_turn_on, topic="Controle.Console")
        log.info("Esperando resposta...")
        try:
            message = channel.consume(timeout=5.0).body.decode("utf-8")
            system = message
            log.info(f"Sistema: {system}")
        except TimeoutError:
            if attempts >= 3:
                log.error("Número máximo de tentativas atingido.")
                break
            attempts += 1
            log.warn("Timeout. Tentando novamente...")
        time.sleep(1)  # Aguardar antes de tentar novamente
            
def menu():
    global system

    if system == 'Off':
        log.info("Verificando se o sistema está ligado...")
        # testando o topico Requisicao.Robo
        req = RequisicaoRobo()
        req.function = "ping"
        channel.publish(Message(content=req, reply_to=name), topic="Requisicao.Robo")
        try:
            time.sleep(1)  # Aguardar um segundo antes de consumir a mensagem
            message = channel.consume(timeout=2.0)
            if message.status.code == StatusCode.INVALID_ARGUMENT:
                system = 'On'
                log.info("Sistema já está ligado.")
                menu()
        except TimeoutError:
            log.info("Sistema está desligado.")

        print("1 - Ligar o sistema")
        print("2 - Sair")
        option = input("Escolha uma opção: ")
        if option == '1':
            turn_on()
            menu()
        elif option == '2':
            log.info("Saindo...")
            exit()
        else:
            log.error("Opção inválida.")
            menu()
    else:
        print("1 - Pegar posição de um robô")
        print("2 - Setar posição de um robô")
        print("3 - Sair")
        option = input("Escolha uma opção: ")
        if option == '1':
            id = int(input("Digite o ID do robô: "))
            choosing_robot("get_position", id=id)
            menu()
        elif option == '2':
            id = int(input("Digite o ID do robô: "))
            x = int(input("Digite a posição X: "))
            y = int(input("Digite a posição Y: "))
            z = int(input("Digite a posição Z: "))
            choosing_robot("set_position", id=id, x=x, y=y, z=z)
            menu()
        elif option == '3':
            log.info("Saindo...")
            exit()
        else:
            log.error("Opção inválida.")
            menu()

while True:
    menu()
