# Escolhendo uma imagem base leve com Python
FROM python:3.9-slim

# Diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos de dependências
COPY requirements.txt /app/

# Instalar as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o contêiner
COPY . /app

# Definir as variáveis de ambiente padrão para o código
ENV IP="localhost:5672"
ENV DEFAULT_TOPIC="default_topic"

# Comando padrão para rodar o publicador
CMD ["python", "pub.py"]
