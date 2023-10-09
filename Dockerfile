FROM python:3.11-alpine
ENV FLASK_APP flask-chat.py
ENV FLASK_CONFIG docker

RUN adduser -D admin 
USER admin

WORKDIR /home/admin

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
