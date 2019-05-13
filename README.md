# Locus

Components supporting discovery of information flow based on similarity and citation analysis.

## Table of Contents
- [Features](#features)
- [Usage](#usage)
- [Built-With](#built-with)
- [Authors](#authors)

## Features
* 

## Usage

### Prerequisites

#### Redis server (for channel layer backend)
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
### Start
Run workers for searching components:
```
python manage.py runworker tweet_crawler
```
Start server:
```
python manage.py runserver
```
               
## Built-With
* [Twint](https://github.com/twintproject/twint) - Twitter Intelligence Tool
* [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines
* [Django Channels](https://channels.readthedocs.io/en/latest/) - Extends Django to handle WebSockets, chat protocols, IoT protocols, and more

## Authors
* Aleksandra Mazur
* Mateusz Buta
