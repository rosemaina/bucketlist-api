[![Coverage Status](https://coveralls.io/repos/github/rosemaina/bucketlist-api/badge.svg?branch=feature)](https://coveralls.io/github/rosemaina/bucketlist-api?branch=feature)

# Bucketlist-api
A bucketlist is a list of activites that one aspires to do before they kick the bucket.
This is a python flask based RESTful API application that allows users to Create, Read, Update, Delete bucketlist and bucketlist items/ activities

A flask based API application that gives users the opportunity to create, update, delete and view bucket list items. bucket list items are wishes users wish to accomplish before kicking the bucket. #API Endpoints

POST /auth/login login a user
POST /auth/register register a user
POST /bucketlist create a bucketlist
GET /bucketlist view created bucketlists
GET /bucketlist/<id> view a specific bucketlist
PUT /bucketlist/<id> update a specific bucketlist
DELETE /bucketlist/<id> delete a specific bucketlist
POST /bucketlist/<id>/items/ create a bucketlist item
PUT /bucketlist/<id>/items/<item_id> update a specific bucketlist item
DELETE /bucketlist/<id>/items/<item_id> delete a specific bucketlist item  

Requirements

python 3.4, 3.6  
virtualenv  
autoenv  

Installation  

Download the project locally by running : git clone https://github.com/rosemaina/bucketlist-api.git  
cd bucketlist-api  
create a virtualenv file. bucketenv  
create a .env file and add the following exports:
source bucketenv/bin/activate  
export APP_SETTINGS=development  
export SECRET=<your SECRET-KEY-here-some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING>  
save the file  
Install the requirements in the requirements.txt file. Run pip install -r requirements.txt  
Run the application. python run.py  
Testing  

To run tests against the project run: nosetests  

#Contributors

Rose Maina
