[![Coverage Status](https://coveralls.io/repos/github/rosemaina/bucketlist-api/badge.svg?branch=feature)](https://coveralls.io/github/rosemaina/bucketlist-api?branch=feature)
[![Build Status](https://travis-ci.org/rosemaina/bucketlist-api.svg?branch=master)](https://travis-ci.org/rosemaina/bucketlist-api)

# Bucketlist-api
A bucketlist is a list of activites that one aspires to do before they kick the bucket.
This is a python flask based RESTful API application that allows users to Create, Read, Update, Delete bucketlist and bucketlist items/ activities

#API Endpoints

1. 'POST /auth/login` login a user

2. `POST /auth/register` register a user

3. `POST /bucketlist create a bucketlist

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

. create a virtualenv file. bucketenv

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
