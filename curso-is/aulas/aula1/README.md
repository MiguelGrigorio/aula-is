# Docker

## O que são containers?

Container é o nome dado para a segregação de processos no mesmo kernel, de forma que o processo
seja isolado o máximo possível de todo o resto do ambiente.
Em termos práticos são File Systems, criados a partir de uma "imagem" e que podem possuir
também algumas características próprias.

## O que são imagens Docker ?

Uma imagem Docker é a materialização de um modelo de um sistema de arquivos, modelo este
produzido através de um processo chamado build.
Esta imagem é representada por um ou mais arquivos e pode ser armazenada em um repositório.

## Construção de uma imagem

Processo para gerar uma nova imagem a partir de um arquivo de instruções. O comando docker
build é o responsável por ler um Dockerfile e produzir uma nova imagem Docker.

## Exemplo

Aplicação: Um servidor em flask que exibe o texto "Bem vindo ao curso do IS" [ao clicar aqui](http://127.0.0.1:8080/Boas-vindas).
A aplicação completa encontra-se no diretório /exemplo.

### Image

- Requirements: flask==2.0.1

- Dockerfile:

```
FROM python:3.7-alpine
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

```
- Build the image:

```
docker build --tag=flaskboasvindas .
```
### Containers
- Run the Container

```  
sudo docker run -it --rm --name flaskboasvindasContainer -p 8080:8000 flaskboasvindas python3 serverFlask.py
```

## Outros repositórios

- [Exemplo do luiz](https://github.com/luizcarloscf/docker-basic)
- [Trabalho final da disciplina laboratorio de redes](https://github.com/matheusdutra0207/MonitoringLabRedes)
- [Google](https://cloud.google.com/containers)

