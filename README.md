# Flask-Chat

![](https://github.com/Oxmoon/flask-chat/blob/main/images/Screenshot.png?raw=true)

## Description

A live chatting site example using:

### [Flask](https://flask.palletsprojects.com/en/3.0.x/) | [SQLAlchemy](https://docs.sqlalchemy.org/en/20/index.html) | [PostgreSQL](https://www.postgresql.org/) | [Javascript SocketIO](https://socket.io/docs/v4/) | [Gunicorn](https://gunicorn.org/) | [Docker](https://www.docker.com/) | [Bootstrap 3.0](https://getbootstrap.com/docs/3.3/)

## Installation

### Unix/macOS

To run this app in a docker container your machine will require Docker, Git, and Python3.11, virtualenv, and available on the commandline.

If you have python3 installed but not virtualenv, you can install it with: `python3 -m pip install --user virtualenv`

```
git clone https://github.com/Oxmoon/flask-chat.git
cd flask-chat/
python3 -m venv .venv
. .venv/bin/activate
pip install -r ./requirements/docker.txt
```

All database usernames, passwords, and the flask app secret key are saved in the `.env` file. Edit them now if you like before moving on to the next step.

```
# This script creates the users for the psql database.
./install.sh
```

If the bash script does not run, change the permissions with: `chmod +x ./install.sh`

```
docker-compose up -d --build
```

If you want to access the database from the commandline use: `docker exec -it flask-chat-db-1 bash`

Once up, the site will be available from http://localhost:8000/

## License

Copyright © 2023 [Gage Hilyard](https://github.com/Oxmoon/).  
This project is [MIT licensed](LICENSE.md).

