from is_wire.core import Channel, Message
from is_msgs.image_pb2 import Image
import cv2
import numpy as np
import time


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

try:
    #load_dotenv()
    ip = "10.10.0.91:5672"# ip:porta

    # Conectando ao broker
    channel = Channel(f"amqp://guest:guest@{ip}")
    
    # Cria a mensagem
    message = Message()

    # Define quem enviou a mensagem
    message.reply_to = input("Digite seu nome: ")

    # Define o tópico
    topico = "atividadeKubernetes"
    print("\n")

    while True:
        # Define qual a mensagem e o destinatário
        path_image = "pub-sub-images/pub/image.jpeg" #input("Digite o caminho da imagem: ")

        # Abre a imagem
        img = cv2.imread(path_image)

        # Cria o pacote da imagem
        message.pack(to_image(img))

        dest = "images"
        
        # Envia a mensagem para o destinatário do tópico
        channel.publish(message, topic = f"{topico}.{dest}")
        print("Imagem enviada.")
        time.sleep(1)

except KeyboardInterrupt:
	print("\nSaindo...")

except ConnectionError:
	print("\nErro ao conectar ao broker.")

except Exception as e:
	print(f"\nErro: {e}")
