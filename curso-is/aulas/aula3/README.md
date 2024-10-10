# is-msgs
- [Laboratório de Visão Computacional e Robótica - LabVISIO](https://github.com/labviros)
- [is-msgs](https://github.com/labviros/is-msgs)

## Exemplos

#### 1. Declarar uma variável do tipo "CameraSettings"(encontra-se no repositório do is-msgs). A variável terá que ter os campos brightness, saturation e zoom preenchidos com False no campo automatic e 0.2, 0.7, 0.8 no campo ratio respectivamente.

1. Fazer o import da classe “CameraSettings”.
```
from is_msgs.camera_pb2 import CameraSettings
```
2. Vamos precisar da classe “CameraSetting” para resolver o exercício, pois os tipos dos campos da classe “CameraSettings” é “CameraSetting”.

```
from is_msgs.camera_pb2 import CameraSetting
```

3. Declaração de 3 variáveis do tipo "CameraSetting".

```
brightness = CameraSetting()
saturation = CameraSetting()
zoom = CameraSetting()
```

4. Abaixo, ocorre a atribuição dos valores. Observe que no campo “automatic” aceita-se o tipo bool e o campo ratio o tipo “float”.
```
brightness.automatic = False
saturation.automatic = False
zoom.automatic = False

brightness.ratio = 0.2
saturation.ratio = 0.7
zoom.ratio = 0.8
```
5. Criação da variável do tipo "CameraSettings" e passagem dos valores declarados para os respectivos campos.
```
camera = CameraSettings(
    brightness=brightness,
    saturation=saturation,
    zoom=zoom
    )
```

6. Acessando os valores declarados.
```
print(camera)
print(camera.brightness)
print(camera.saturation.automatic)
```
7. Código completo.
```
from is_msgs.camera_pb2 import CameraSettings
from is_msgs.camera_pb2 import CameraSetting

brightness = CameraSetting()
saturation = CameraSetting()
zoom = CameraSetting()

brightness.automatic = False
saturation.automatic = False
zoom.automatic = False

brightness.ratio = 0.2
saturation.ratio = 0.7
zoom.ratio = 0.8

camera = CameraSettings(
    brightness=brightness,
    saturation=saturation,
    zoom=zoom
    )

print(camera)
print(camera.brightness)
print(camera.saturation.automatic)```

```


