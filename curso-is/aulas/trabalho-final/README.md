# Trabalho Final

![Trabalho Final](https://github.com/matheusdutra0207/TrabalhoFinal/blob/main/trabalho%20final/alunos-is.png)

# Construindo a mensagem RequisicaoRobo

## 1. Montar o arquivo RequisicaoRobo.proto

```
syntax = "proto3";

package is.robot;

option java_package = "com.is.robot";
option java_multiple_files = true;

import "is/msgs/common.proto";

message RequisicaoRobo {

  int64 id = 1;

  string function = 2;

  common.Position positions = 3;

}
```
## 2. Executar o comando

```
python -m is_msgs.utils.build RequisicaoRobo.proto
```

## 3. Pronto, agora é só usar a classe

```
from RequisicaoRobo_pb2 import RequisicaoRobo
```


