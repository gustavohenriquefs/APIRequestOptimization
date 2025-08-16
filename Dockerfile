# Use uma imagem base oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos de requirements primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY src/ ./src/
COPY main.py .

# Define as variáveis de ambiente
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expõe a porta 5000
EXPOSE 5000

# Define o usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash app_user
USER app_user

# Comando para executar a aplicação
CMD ["python", "main.py"]
