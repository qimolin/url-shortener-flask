# URL Shortener Flask

This repo is part of the UvA course Web Services and Cloud-Based Systems. It is a simple URL shortener service implemented in Flask.

## Create a venv
```bash
python -m venv .venv
. .venv/bin/activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the app (with reload)
```bash
flask run --reload
```

## Install redis-cli
```bash
brew install redis
```

## Start redis server
```bash
redis-server
```

## Query redis
```bash
redis-cli -h localhost -p 6379
```

## Build and run the docker container
```bash
docker build -t url-shortener-flask .
docker run -p 5000:5000 url-shortener-flask
```