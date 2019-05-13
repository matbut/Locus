# Locus

Components supporting discovery of information flow based on similarity and citation analysis

## Prerequisites

### Redis server (for channel layer backend)
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
## Start
Run workers for searching components:
```
python manage.py runworker tweet_crawler
```
Start server:
```
python manage.py runserver
```
