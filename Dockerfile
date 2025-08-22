# Base Ubuntu
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

# Atualiza e instala dependências mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3-pip \
    mysql-client \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Instala libs Python direto (exemplo)
RUN python3.11 -m pip install --upgrade pip \ 
&& python3.11 -m pip install schedule
