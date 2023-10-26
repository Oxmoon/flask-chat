#!/bin/sh
source .venv/bin/activate
flask deploy
exec gunicorn -b 0.0.0.0:5000 --timeout 5 --worker-class=gevent flask-chat:app
