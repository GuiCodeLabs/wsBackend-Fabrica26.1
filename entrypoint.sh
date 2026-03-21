#!/bin/sh

# Aplica as migrações no banco de dados automaticamente
echo "Aplicando migrações..."
python manage.py migrate

# Executa o comando passado no CMD do Dockerfile
exec "$@"