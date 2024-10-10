# Pub e Sub com imagens

Funciona de forma semelhante ao [chat][1], entretanto, enviar mensagens que contém imagem não é possível enviar de forma direta, então é necessário converter a imagem para uma forma codificada e depois decodificar ela quando receber.

No [pub.py][2]:
```py
def to_image(input_image, encode_format='.jpeg', compression_level=0.8):
    if isinstance(input_image, np.ndarray):
        if encode_format == '.jpeg':
            params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
        elif encode_format == '.png':
            params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format, img=input_image, params=params)
        return Image(data=cimage[1].tobytes())
    elif isinstance(input_image, Image):
        return input_image
    else:
        return Image()
```

No [sub.py][3]:

```py
def to_np(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image
```
[1]: chat-com-rabbitmq/README.md
[2]: pub-sub-images/pub/pub.py
[3]: pub-sub-images/sub/sub.py