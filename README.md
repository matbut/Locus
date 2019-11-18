# Locus

Components supporting discovery of information flow based on similarity and citation analysis.

## Table of Contents
<!-- - [Features](#features) -->
- [Usage](#usage)
- [Built-With](#built-with)
- [Authors](#authors)

<!--
## Features
* 
-->

## Usage

### Requirements

#### Python
Version 3.7.3

#### Redis server 
<!-- (for channel layer backend) -->
Installation guide can be found at: https://redis.io/topics/quickstart. <br/>
Run server:
```
redis-server
```
Check if Redis is working properly by sending a PING command:
```
$ redis-cli ping
PONG
```

#### PostgreSQL
It can be installed with:
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Installing
We recommend to create virtual environment with [venv](https://docs.python.org/3/library/venv.html)
```
git clone git@github.com:matbut/Locus.git
pip3 install -r requirements.txt 
npm install
```

### Setup
Before running application for the first time it is required to run the script setup.sh
```
cd locus_project
./setup.sh
``` 

### Start
Run worker for searching components:
```
python3 manage.py runworker tweet_crawler google_crawler db_searcher
```
Start server:
```
python3 manage.py runserver
```
               
## Built-With
* [Twint](https://github.com/twintproject/twint) - Twitter Intelligence Tool
* [Django](https://www.djangoproject.com/) - Python web development framework
* [Django Channels](https://channels.readthedocs.io/en/latest/) - Extends Django to handle WebSockets

## Authors
* Aleksandra Mazur
* Mateusz Buta
