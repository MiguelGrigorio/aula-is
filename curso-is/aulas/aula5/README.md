# logs
O [log](https://www.youtube.com/watch?v=tZ2iJ5H99fg&t=2641s&ab_channel=EduardoMendes) é um meio de rastrear eventos que acontecem quando algum software é executado. Eles fornecem uma explicação simples de algum evento no sistema separando em níveis diferentes certos tipos de mensagens.

Os [logs no espaço inteligente](https://github.com/labviros/is-wire-py/blob/master/src/is_wire/core/logger.py) são configurados através da classe Logger (from is_wire.core import Logger). 

## Logger

```
from is_wire.core import Logger

log = Logger(name = "Teste")

log.debug("Um debug")

log.info("olá :)")

log.warn("cuidado")

log.error("Ops")

#### Esse Logger encerra o programa

log.critical("erro crítico")

print("Não será exibido")
```

![Resultado](https://github.com/matheusdutra0207/logs/blob/main/M%C3%ADdia/log1.JPG "result")

# Status

[Status suportados pelo IS](https://github.com/labviros/is-wire-py/blob/master/src/is_wire/core/wire/status.py)

## Exemplo de aplicação de Status em uma função

```
from is_wire.core import StatusCode, Status
from google.protobuf.struct_pb2 import Struct
from is_wire.core import Logger

log = Logger(name = "root")

def increment(struct):
    if struct.fields["value"].number_value < 0:
        return Status(StatusCode.INVALID_ARGUMENT, "Number must be positive")

    struct.fields["value"].number_value += 1.0
    return struct

#Observem os resultados 
struct_1 = Struct()
struct_2 = Struct()

struct_1.fields["value"].number_value = 1.0
struct_2.fields["value"].number_value = -1.0


print(increment(struct_1))
print(increment(struct_1).fields["value"].number_value)


print(increment(struct_2))
print(increment(struct_2).code)

```






