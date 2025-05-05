#!/bin/sh

docker kill dev_db-postgres-1
docker rm dev_db-postgres-1
sudo rm -r ./gitignore
