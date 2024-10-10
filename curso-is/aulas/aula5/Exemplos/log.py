from is_wire.core import Logger

log = Logger(name = "Teste")

log.debug("Um debug")

log.info("olá :)")

log.warn("cuidado")

log.error("Ops")

#### Esse Logger encerra o programa

log.critical("erro crítico")

print("Não será exibido")
