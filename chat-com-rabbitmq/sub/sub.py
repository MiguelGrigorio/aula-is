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

	# Define quem está subscrevendo
	dest = input("Digite seu nome: ")

	# Define o tópico
	topico = input("Digite o tópico que deseja subscrever: ")

	# Subscreve para o tópico
	sub.subscribe(topic = f"{topico}.{dest}")
	print("\n")

	while True:
		# Recebe a mensagem
		message = channel.consume()
		print(message.reply_to + ": " + message.body.decode("utf-8"))
		time.sleep(1)

except KeyboardInterrupt:
	print("\nSaindo...")

except ConnectionError:
	print("\nErro ao conectar ao broker.")

except Exception as e:
	print(f"\nErro: {e}")