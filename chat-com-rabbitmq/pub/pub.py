from is_wire.core import Channel, Message
from dotenv import load_dotenv
import os

try:
	load_dotenv()
	ip = os.getenv("IP") # ip:porta

	# Conectando ao broker
	channel = Channel(f"amqp://guest:guest@{ip}")

	# Cria a mensagem
	message = Message()

	# Define quem enviou a mensagem
	message.reply_to = input("Digite seu nome: ")

	# Define o tópico
	topico = input("Digite o tópico que deseja enviar: ")
	print("\n")

	while True:
		# Define qual a mensagem e o destinatário
		mensagem = input("Digite sua mensagem: ")
		dest = input("Digite seu destino: ")

		# Codifica a mensagem
		message.body = mensagem.encode("utf-8")
		print("")

		# Envia a mensagem para o destinatário do tópico
		channel.publish(message, topic = f"{topico}.{dest}")

except KeyboardInterrupt:
	print("\nSaindo...")

except ConnectionError:
	print("\nErro ao conectar ao broker.")

except Exception as e:
	print(f"\nErro: {e}")