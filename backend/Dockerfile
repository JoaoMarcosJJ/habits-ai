FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para compilar alguns pacotes Python
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# O comando de execução está no docker-compose