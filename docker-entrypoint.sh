#!/bin/bash

echo "Aguardando PostgreSQL ficar disponível..."

until PGPASSWORD=postgres psql -h postgres -U postgres -d financeiro -c '\q'; do
    echo "PostgreSQL ainda não disponível..."
    sleep 2
done

echo "PostgreSQL disponível!"

TABLE_EXISTS=$(PGPASSWORD=postgres psql -h postgres -U postgres -d financeiro -tAc "
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'usuarios'
);
")

if [ "$TABLE_EXISTS" = "f" ]; then
    echo "Banco vazio. Executando defaultDatabase.sql..."

    PGPASSWORD=postgres psql \
        -h postgres \
        -U postgres \
        -d financeiro \
        -f /app/app/schema/defaultDatabase.sql
else
    echo "Banco já inicializado. Pulando Default script SQL."
fi

echo "Inicializando aplicação Flask..."

python app.py