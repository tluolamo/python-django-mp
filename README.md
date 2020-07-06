Readme

This API uses Celery with Redis backend to handle file processing asynchronously.

To get up and running:

Make sure redis is running in port 6379, easy way to get it going is to use the redis docker image https://hub.docker.com/_/redis

Configure the DB you want to use by adjusting the mp_aps/settings.py file, if no change is made it'll use sqlite3. But any SQL backend can be put in its place.

Setup DB `./manage.py migrate`

Run Django locally `./manage.py runserver` 
