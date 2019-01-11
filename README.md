# Powtoon assignment task

## Dependencies
* Docker
* Docker-compose

### For running it locally
docker-compose up

### For creating superuser inside docker machine
docker exec -it powtoon_web python manage.py createsuperuser

### For running tests
docker exec -it powtoon_web python manage.py test

### For terminating whole stack
docker-compose down --rmi all --volumes
