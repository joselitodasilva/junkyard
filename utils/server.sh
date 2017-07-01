uwsgi --plugin python -s 0.0.0.0:8080 --protocol=http -w junkyard:app
