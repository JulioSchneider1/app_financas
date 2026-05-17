#!/bin/bash

echo "Aguardando PostgreSQL ficar disponível..."

until PGPASSWORD=postgres psql -h postgres -U postgres -d financeiro -c '\q'; do
    echo "PostgreSQL ainda não disponível..."
    sleep 2
done

echo "PostgreSQL disponível!"

echo "Executando defaultDatabase.sql..."

PGPASSWORD=postgres psql -h postgres -U postgres -d financeiro -f /app/schema/defaultDatabase.sql

echo "Inicializando aplicação Flask..."

python app.py