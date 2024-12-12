from is_wire.core import Channel, Logger, Subscription
from is_msgs.image_pb2 import Image
import numpy as np
import cv2
import os


def to_np(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image

name = "sub"
log = Logger(name)

try:
    # Configurado via ConfigMap
    log.info("Carregando variáveis de ambiente...")
    ip = os.getenv("IP", "10.10.0.91:5672")
    topic = os.getenv("TOPIC", "image")

    log.info("Verificando se possui a pasta data...")
    if not os.path.exists("/app/data"):
        os.makedirs("/app/data")

    # Conectando ao broker
    log.info("Conectando ao broker...")
    channel = Channel(f"amqp://guest:guest@{ip}")

    # Subscreve para o canal
    sub = Subscription(channel)

    # Define quem está subscrevendo
    dest = "sub"

    # Subscreve para o tópico
    sub.subscribe(topic=f"{topic}.{dest}")
    log.info(f"Subscrito para o tópico {topic}.{dest}. Esperando mensagens...")

    # Número de imagens
    i = 0
    while True:
        # Recebe a imagem
        message = channel.consume()
        log.info("Imagem recebida.")
        pack_image = message.unpack(Image)
        image_numpy = to_np(pack_image)

        filename = f"/app/data/image_{i}.jpeg"
        cv2.imwrite(filename, image_numpy)
        log.info('Imagem salva como ' + filename)
        i += 1

except KeyboardInterrupt:
    log.error("\nSaindo...")

except ConnectionError:
    log.error("\nErro ao conectar ao broker.")

except Exception as e:
    log.error(f"\nErro: {e}")
