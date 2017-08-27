[![Coverage Status](https://coveralls.io/repos/github/rosemaina/bucketlist-api/badge.svg?branch=feature)](https://coveralls.io/github/rosemaina/bucketlist-api?branch=feature)
[![Build Status](https://travis-ci.org/rosemaina/bucketlist-api.svg?branch=master)](https://travis-ci.org/rosemaina/bucketlist-api)

# Bucketlist-api
A bucketlist is a list of activites that one aspires to do before they kick the bucket.
This is a python flask based RESTful API application that allows users to Create, Read, Update, Delete bucketlist and bucketlist items/ activities

#API Endpoints

1. `POST /auth/login` login a user

2. `POST /auth/register` register a user

3. `POST /bucketlist` create a bucketlist

4. `GET /bucketlist` view all created bucketlists

5. `GET /bucketlist/<id>` view a specific bucketlist

6. `PUT /bucketlist/<id>` update a specific bucketlist

7. `DELETE /bucketlist/<id>` delete a specific bucketlist

8. `POST /bucketlist/<id>/items` create a bucketlist item

9. `PUT /bucketlist/<id>/items/<item_id>` update a specific bucketlist item

10. `DELETE /bucketlist/<id>/items/<item_id>` delete a specific bucketlist item  

Requirements

python 3.4, 3.6  
virtualenv  
autoenv  

Installation  

Download the project locally by running : git clone https://github.com/rosemaina/bucketlist-api.git  
. `cd bucketlist-api` 

. create a virtualenv file `virtualenv -p python3 bucketenv`

. create a .env file and add the following exports:

. `source bucketenv/bin/activate`

. `export APP_SETTINGS=development`

. `export SECRET=<your SECRET-KEY-here-some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING>`

. save the file

. Install the requirements in the requirements.txt file. Run `pip install -r requirements.txt`

. Run the application. `python manage.py runserver`

Testing  

To run tests against the project run: `coverage run --omit="*/site-packages/*" manage.py test`

#Contributors

Rose Maina

#Acknowledgements
Andela - Inspiring the idea


URL Endpoint    |               HTTP Request   | Resource Accessed | Access Type|
----------------|-----------------|-------------|------------------
/api/bucketlists/auth/register   |      POST    | Register a new user|publc
/api/bucketlists/auth/login      |     POST    | Login and retrieve token|public
/api/bucketlists/auth/logout      |     POST    | Logout and thus deactivate token|public
/api/bucketlists/auth/reset-password      |     PUT    | Reset your password when logged in|private
/api/bucketlists                  |      POST    |Create a new Bucketlist|private
/api/bucketlists                  |      GET    |     Retrieve all bucketlists for user|private
/api/bucketlists/<buckelist_id>            |      GET        | Retrieve a bucketlist by ID | private
/api/bucketlists/<bucketlist_id>              |      PUT    |     Update a bucketlist |private
/api/bucketlists/<bucketlist_id>              |      DELETE    | Delete a bucketlist |private
/api/bucketlists/<bucketlist_id>/items/  |           GET    |Retrive items in a given bucket list|private
/api/bucketlists/<bucketlist_id>/items/     |     POST    | Create items in a bucketlist |private
/api/bucketlists/<bucketlist_id>/items/<item_id>|    DELETE    | Delete an item in a bucketlist |prvate
/api/bucketlists/<bucketlist_id>/items/<item_id>|    PUT       |update a bucketlist item details |private
