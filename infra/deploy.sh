eval $(docker-machine env lecopain-aws)
docker pull pierrickm/flask-lecopain
docker-compose up --force-recreate --build -d
docker image prune -f