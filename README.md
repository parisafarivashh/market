# market
*
*
*


# Dockerizing Django with Postgres, Gunicorn, and Nginx
* Dockerfile : Your Docker workflow should be to build a suitable Dockerfile for each image you wish to create
  - PYTHONDONTWRITEBYTECODE : Prevents Python from writing pyc files to disc
  - PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
  - in docker file:
     - install psycopg2 dependencies
     ```bash
      RUN apk update \
         && apk add postgresql-dev gcc python3-dev musl-dev
      ```
  
  
* Docker compose:   
  - Docker Compose is a tool that was developed to help define and share multi-container applications.
    With Compose, we can create a YAML file to define the services and with a single command, can spin everything up or tear it all down.
    
* entrypoint.sh :
  - add an entrypoint.sh file to the "app" directory to verify that Postgres is healthy before applying the migrations and running the Django development       server
  -
  ```bash
  chmod +x app/entrypoint.sh
  ```
  
* Build the image: 
```bash
docker-compose build
```
* Once the image is built, run the container:
```bash
docker-compose up -d
```
* Run the migrations: 
```bash
docker-compose exec web python manage.py migrate --noinput
```
* Bring down the development containers:
```bash
docker-compose down -v
```
* build the production images and spin up the containers:
```bash
docker-compose -f docker-compose.yml up -d --build
```
```bash
 docker-compose -f docker-compose-prod.yml down -v
```
* check for errors in the logs:
```bash
docker-compose -f docker-compose.yml logs -f
```


