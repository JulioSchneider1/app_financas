#!/bin/bash

# Aborta o script imediatamente se algum comando falhar (exceto o loop until)
set -e

echo "Carregando variáveis de ambiente do arquivo .env..."
if [ -f .env ]; then
    # Exporta as variáveis do arquivo .env para o escopo do script
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "AVISO: Arquivo .env não encontrado no diretório atual!"
fi

echo "Aguardando PostgreSQL ($DB_HOST:$DB_PORT) ficar disponível..."

# Desativamos temporariamente o 'set -e' para o loop não quebrar o script na primeira falha
set +e
until PGPASSWORD=$DB_PASSWORD psql \
    -h $DB_HOST \
    -p $DB_PORT \
    -U $DB_USER \
    -d $DB_NAME \
    -c '\q'; do

    echo "PostgreSQL ainda não disponível... Verifique se o banco '$DB_NAME' existe e as credenciais estão corretas."
    sleep 2
done
set -e

echo "PostgreSQL disponível!"

echo "Executando migrations..."
flask --app app.py db upgrade

echo "Populando banco de dados com dados iniciais..."
python seed.py

echo "Inicializando aplicação Flask..."
python app.py