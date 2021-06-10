#!/bin/bash

docker build -t api_flask:latest -f docker/Dockerfile .

if [ "$OSTYPE" = "msys" ]; then
  winpty docker run --rm --name api_flask -d -p 8000:5000 api_flask:latest
else
  docker run --rm --name api_flask -d -p 8000:5000 api_flask:latest
fi
