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