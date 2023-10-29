FROM python:3.11-alpine3.18
ENV FLASK_APP flask-chat.py
ENV FLASK_CONFIG docker

RUN adduser -D admin 
USER admin

WORKDIR /home/admin

COPY requirements requirements
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements/docker.txt
RUN .venv/bin/pip install --upgrade setuptools

COPY app app
COPY migrations migrations
COPY flask-chat.py config.py boot.sh ./

# runtime configuration
EXPOSE 5001
ENTRYPOINT ["./boot.sh"]
