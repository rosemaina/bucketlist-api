[![Coverage Status](https://coveralls.io/repos/github/rosemaina/bucketlist-api/badge.svg?branch=feature)](https://coveralls.io/github/rosemaina/bucketlist-api?branch=feature)
[![Build Status](https://travis-ci.org/rosemaina/bucketlist-api.svg?branch=master)](https://travis-ci.org/rosemaina/bucketlist-api)

# Bucketlist-api
What's on your bucket list? Adventure travel, volunteerism, crazy fun, connecting with nature? 1000+ awesome ideas of things to do before you reach a certain age, year... etc
This is a Python-Flask based RESTful API application that allows users to log and catalog all the stuff they want to accomplish before they expire

### API Documentation
. Link : https://app.swaggerhub.com/apis/rosemaina/bucketlist-api101/1.0.0

## API-ENDPOINTS
URL Endpoint    |               HTTP Request   | Resource Accessed | Access Type|
----------------|-----------------|-------------|------------------
/auth/register   |      POST    | Register a new user |public
/auth/login      |     POST    | Login a registered user |public
/auth/logout      |     POST    | Logout a user |public
/auth/reset-password      |     PUT    | Reset password for a user |private
/bucketlist                  |      POST    | Create a new Bucketlist |private
/bucketlist                  |      GET    |     Retrieve all bucketlists for one user |private
/bucketlist/<id>            |      GET        | Retrieve a specific bucketlist |private
/bucketlist/<id>              |      PUT    |     Update a bucketlist |private
/bucketlist/<id>              |      DELETE    | Delete a bucketlist |private
/bucketlist/<id>/item  |           GET    | Retrieve items for a specific bucketlist |private
/bucketlist/<id>/item    |     POST    | Create items in a bucketlist |private
/bucketlist/<id>/item/<item_id> |    DELETE    | Delete an item in a bucketlist |prvate
/bucketlist/<id>/item/<item_id> |    PUT       | Update a bucketlist item |private


#### Prerequisites:

Postgres  
Flask  
python 3.4,3.5, 3.6  
virtualenv  
autoenv  

#### Installation  

Download the project locally by running : git clone https://github.com/rosemaina/bucketlist-api.git   
. Prepare directory for project code:  

  `$ mkdir -p ~/bucketlist-api`  
  `$ cd ~/bucketlist-api` 

. Create a virtualenv file 

   `$ virtualenv -p python3 bucketenv`  
   `$ source bucketenv/bin/activate`   

. Create a .env file and add the following exports:

. `export APP_SETTINGS=development`

. `export SECRET=<your SECRET-KEY-here-some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING>`

. save the file

. activate environment variables `source .env`

. Install the requirements in the requirements.txt file. Run `pip install -r requirements.txt`

. Create a database  `createdb flask_api;`

. To do migrations;  

. `python manage.py db init`  
  `python manage.py db migrate`  
  `python manage.py db upgrade`  

. Run the application. `python manage.py runserver`  
. The server should be running on server : http://127.0.0.1:5000/  

#### Testing  

To run tests against the project run: `nosetests  --with-coverage --cover-package=app`

### Deployment

Link : https://bucketlist-api1.herokuapp.com/  
To deploy your a copy of your application to heroku. Run `heroku create <your_url_name>`

### Contributors

Rose Maina

### Acknowledgements

Andela - Inspiring the idea


