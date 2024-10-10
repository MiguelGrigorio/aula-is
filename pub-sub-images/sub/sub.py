from is_wire.core import Channel, Subscription, Message
from is_msgs.image_pb2 import Image
import numpy as np
import cv2
from dotenv import load_dotenv
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


try:
    load_dotenv()
    ip = os.getenv("IP") # ip:porta

	# Conectando ao broker
    channel = Channel(f"amqp://guest:guest@{ip}")

	# Subscreve para o canal
    sub = Subscription(channel)

	# Define quem está subscrevendo
    dest = input("Digite seu nome: ")

	# Define o tópico
    topico = input("Digite o tópico que deseja subscrever: ")

	# Subscreve para o tópico
    sub.subscribe(topic = f"{topico}.{dest}")
    print("\n")

    while True:
        # Recebe a imagem
        message = channel.consume()
        pack_image = message.unpack(Image)
        image_numpy = to_np(pack_image)

        filename = input(f"Digite o nome do arquivo para salvar a imagem de {message.reply_to}: ") + ".jpeg"
        cv2.imwrite(filename, image_numpy)
        print('Imagem salva.')
        break

except KeyboardInterrupt:
	print("\nSaindo...")

except ConnectionError:
	print("\nErro ao conectar ao broker.")

except Exception as e:
	print(f"\nErro: {e}")
