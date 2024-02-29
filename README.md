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
python app.py --reload
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

## Test data percistency locally: 
1- run `docker-compose up -d`
2- run tests to populate data `python3 test_app.py`
3- test data persists after running `docker-compose restart`
  - `docker exec -it url-shortener-flask-redis-1 sh`
  - `redis-cli`
  - `KEYS *`

- To test url shortening service from local machine using contol node's IP `145.100.135.145` and the NodePort exposed for the Ingress controller `31660` using curl:

- create user:
curl -X POST http://145.100.135.145:31660/auth/users -H "Content-Type: application/json" -d '{"username":"my_username3", "password":"my_password3"}'

- login:
curl -X POST http://145.100.135.145:31660/auth/users/login -H "Content-Type: application/json" -d '{"username":"my_username3", "password":"my_password3"}'

- create short url with the returned <token>
curl -X POST http://145.100.135.145:31660/ -H "Content-Type: application/json" -H "Authorization: Bearer <token>” \
-d '{"value": "https://example12.com”}’

- to check redis db `kubectl exec -it <redis-deployment-pod> -- redis-cli`

## Test endpoints using Postman
- Import the environment `Cluster.postman_environment.json` to Postman
- Import the environment `Local.postman_environment.json` to Postman
- Import the collection `URL Shortener.postman_collection.json` to Postman
- Run the collection to test the endpoints
- You will have to call the [auth service](https://github.com/qimolin/auth-service-flask) to get the token and use it in the headers of the other requests
- Note: you can switch between the environments to test the endpoints on the local machine or the cluster