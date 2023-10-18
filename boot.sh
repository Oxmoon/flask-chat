#!/bin/sh
source .venv/bin/activate
flask db migrate
flask deploy
exec gunicorn -b 0.0.0.0:5000 --log-level debug --timeout 5 --worker-class=gevent --workers 4 flask-chat:app
