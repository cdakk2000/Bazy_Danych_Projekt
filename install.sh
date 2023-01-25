#!/bin/sh
sleep 10
if [ ! -f /setup-done ]; then

cd /app
python init-db.py

cd /app/import_phone_data/
python import_data.py

cd /app
python manage.py migrate

touch /setup-done
fi

cd /app
exec python manage.py runserver 0.0.0.0:8000