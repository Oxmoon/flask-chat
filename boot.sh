#!/bin/sh
source .venv/bin/activate
flask deploy
exec gunicorn -b 0.0.0.0:5000 --worker-class=gevent --workers 4 --access-logfile - --error-logfile - flask-chat:app
