from is_wire.core import Channel, Subscription
import time
from dotenv import load_dotenv
import os

try:
	load_dotenv()
	ip = os.getenv("IP") # ip:porta

	# Conectando ao broker
	channel = Channel(f"amqp://guest:guest@{ip}")

	# Subscreve para o tópico
	sub = Subscription(channel)
	dest = input("Digite seu nome: ")
	topico = input("Digite o tópico que deseja subscrever: ")
	sub.subscribe(topic = f"{topico}.{dest}")
	print("\n")

	while True:
		message = channel.consume()
		print(message.reply_to + ": " + message.body.decode("utf-8"))
		time.sleep(1)

except KeyboardInterrupt:
	print("\nSaindo...")

except ConnectionError:
	print("\nErro ao conectar ao broker.")

except Exception as e:
	print(f"\nErro: {e}")