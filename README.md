# market
* User can signup/login/logout
  - the user`s phone number is unique
  - wallet and basket are create as the same time as the user login
  - welcome massage is sent to the user`s websocket(uses websocket)
  - user has the profile(user can update own profile)
* Chat messaging: User can send direct message to another user
  - Direct created between reciver and creator user
  - When user sends message to other.. her message also sent from websocket 
  - push-notification also sent from websocket for user that who receive message
  - Users can see a list of messages they have sent to different directs. user can delete or update self message
  
* There are Product, subcategory and category and detail for models
  - everyone that who authenticated can upload self product(products can have different colors or different size and price )
  - everyone without authenticated can see list products(there are filtering and search for product)
  - just the creator of the product can change the price or something from the product
* Users can choose products to buying
  - there are order and itemorder models 
  - users can add products to self basket also update the count of that
  - users can see self-order and total price or delete some products from the basket 
* Panel admin 
  - admin token has different from user token (admin has jwt token)
  - admins have different permissions and super-admin can give permission to other
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


