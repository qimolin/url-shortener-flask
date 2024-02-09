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

## Run the app
```bash
flask run
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