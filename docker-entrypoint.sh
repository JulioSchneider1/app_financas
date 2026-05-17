#!/bin/bash

echo "Aguardando PostgreSQL ficar disponível..."

until PGPASSWORD=$DB_PASSWORD psql \
    -h $DB_HOST \
    -U $DB_USER \
    -d $DB_NAME \
    -c '\q'; do

    echo "PostgreSQL ainda não disponível..."
    sleep 2
done

echo "PostgreSQL disponível!"

echo "Executando migrations..."

flask --app app.py db upgrade

echo "Populando banco de dados com dados iniciais..."

python seed.py

echo "Inicializando aplicação Flask..."

python app.py
