"""This module contains all endpoints"""
# Importing objects from flask
import os
import jwt
from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    """ Wraps the creation of a new Flask object and returns it"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    #loads up config settings
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Connects to the db
    db.init_app(app)
    from app.models import User
    from app.models import Bucketlist
    from app.models import Item


    def token_required(f):
        """This valids token"""
        # this takes in a function f
        @wraps(f)
        # define a function decorated
        def decorated(*args, **kwargs):
            token = None

            # ckecking if auth is in header
            if 'Authorization' in request.headers:
                # reads the token value
                token = request.headers['Authorization']

            if not token:
                # this returns an error when token is missing
                return jsonify({'error': 'Token not found!'}), 401

            try:
                # tying to decode the token found
                #and fetch the user by User.id
                id = jwt.decode(token, os.getenv('SECRET'))['id']
                current_user = User.query.filter_by(id=id).first()
            except:
                return jsonify({'message': 'Token expired!'}), 401

            # returns the functions witht the user and its args
            return f(current_user=current_user, *args, **kwargs)

        return decorated



    @app.route('/auth/register', methods=['POST'])
    def user_registration():
        """Method used to register a user"""
        email = request.data['email']
        password = request.data['password']
        try:
            reg_user = User.query.filter_by(email=email).first()
            if reg_user:
                resp = jsonify({'message': 'Email address already exists!'})
                resp.status_code = 409
                return resp
            if email and password:
                if len(password) >= 8:
                    if User.validate_email(email):
                        new_user = User(email)
                        new_user.create_password(password)
                        new_user.save()
                        resp = jsonify({'message': 'Successful registration!'})
                        resp.status_code = 201
                        return resp
                    else:
                        resp = jsonify({'message': 'Invalid email address!'})
                        resp.status_code = 403
                        return resp
                else:
                    # takes the dic and turns it to a json and adds status code
                    resp = jsonify({'message': 'Password length is too short!'})
                    resp.status_code = 411
                    return resp
            else:
                resp = jsonify({'message': 'Email and password required!'})
                resp.status_code = 400
                return resp
        except:
            resp = jsonify({'error': 'An error occured'})
            resp.status_code = 500
            return resp


    @app.route('/auth/login', methods=['POST'])
    def user_login():
        email = request.data['email']
        password = request.data['password']
        found_user = User.query.filter_by(email=email).first()
        if not found_user:
            resp = jsonify({'error': 'User {} not found'.format(email)})
            resp.status_code = 401
            return resp

        if not found_user.validate_password(password):
            resp = jsonify({'error': 'Wrong password!'})
            resp.status_code = 400
            return resp
        resp = found_user.gen_token()
        resp.status_code = 200
        return resp

    # @app.route('/auth/logout', methods=['POST'])
    # def logout():
    #     email = request.data['email']
    #     password = request.data['password']


    # @app.route('/auth/reset-password', methods=['POST'])

    # # CRUD bucketlist
    @app.route('/bucketlist', methods=['POST', 'GET'])
    @token_required
    def create_bucketlist(current_user):

        title = str(request.data.get('title'))
        user_id = current_user.id
        if request.method == "POST":
            if title.strip(' '):
                striped_title = title.strip(" ")
                bucketlist = Bucketlist.query.filter_by(user_id=current_user.id,
                                                        title=striped_title).first()
                # Create and saves the striped title
                if not bucketlist:
                    new_bucket = Bucketlist(title=striped_title, user_id=user_id)
                    new_bucket.save()
                    response = jsonify({
                        'id': new_bucket.id,
                        'title': new_bucket.title,
                        'date_created': new_bucket.date_created,
                        'date_modified': new_bucket.date_modified
                    })
                    response.status_code = 201
                    return response
                return jsonify({'error': 'Title already taken!'}), 403
            return jsonify({'error': 'Title not given!'})
        else:
            # GETs all bucketlists
            bucketlists = Bucketlist.query.filter_by(user_id=user_id).all()
            if not bucketlists:
                return jsonify({'error': 'No bucketlists found!'}), 403

            results = []
            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            resp = jsonify(results)
            resp.status_code = 200
            return resp

    @app.route('/bucketlist/<id>', methods=['GET'])
    @token_required
    def get_bucket(current_user, id):
        """Retrieves a buckelist using it's ID"""
        bucketlist = Bucketlist.query.filter_by(user_id=current_user.id, id=id).first()
        if not bucketlist:
            return jsonify({'error': 'Bucketlist NOT found'}), 401
        else:
            # print(bucketlist.items)
            # bucketlist_items = Item.query.filter_by(bucket_id=id)
            # query all bucketlist items with the bucket id
            resp = {
                'id': bucketlist.id,
                'title': bucketlist.title,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                # 'items': { items }
            }
            return jsonify(resp), 200

    @app.route('/bucketlist/<id>', methods=['DELETE'])
    @token_required
    def delete_bucket(current_user, id):
        """Deleting a specific bucketlist"""
        # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(user_id=current_user.id, id=id).first()
        if not bucketlist:
            return jsonify({'error': 'Bucketlist NOT found'}), 401
        else:
            title = bucketlist.title
            bucketlist.delete()
            return jsonify({'message': 'Bucketlist {} deleted'.format(title)})

    @app.route('/bucketlist/<id>', methods=['PUT'])
    @token_required
    def edit_bucket(current_user, id):
        """Edits a bucketlist"""
        if request.method == 'PUT':
            title = str(request.data.get('title'))
            bucketlist = Bucketlist.query.filter_by(user_id=current_user.id, id=id).first()
            if not bucketlist:
                return jsonify({'message': 'Bucketlist NOT found'})
            else:
                bucketlist.title = title
                bucketlist.save()
                resp = {
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                return jsonify(resp), 200
        else:
            # GET
            resp = jsonify({
                'id': bucketlist.id,
                'title': bucketlist.title,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            resp.status_code = 200
            return resp


    # CRUD BUCKET LIST ITEMS
    @app.route('/bucketlist/<id>/item', methods=['POST', 'GET'])
    @token_required
    def create_item(current_user, id):
        """Method creates an item"""
        name = request.data['name']
        bucket_id = id
        if request.method == "POST":
            if name.strip(' '):
                striped_name = name.strip(" ")
                item = Item.query.filter_by(bucket_id=id, name=striped_name).first()
                if not item:
                    new_item = Item(name=striped_name, bucket_id=bucket_id)
                    new_item.save()
                    resp = jsonify({
                        'id': new_item.id,
                        'name': new_item.name,
                    })
                    resp.status_code = 201
                    return resp
                return jsonify({'error': 'Name already exists'}), 403
            return jsonify({'error': 'Item name not given!'})
        # else:
        #     # GETs all items in a list
        #     items = Item.query.filter_by(bucket_id=id).all()
        #     if not items:
        #         return jsonify({'error': 'No bucket items found!'}), 403

        #     results = []
        #     for item in items:
        #         obj = {
        #             'id': item.id,
        #             'name': item.name
        #         }
        #         results.append(obj)
        #     resp = jsonify(results)
        #     resp.status_code = 200
        #     return resp
        
    @app.route('/bucketlist/<id>/item/<item_id>', methods=['DELETE'])
    @token_required
    def delete_bucketlist_item(current_user, id, item_id):
        """"Deltes a bucketlist"""
        item = Item.query.filter_by(bucket_id=id, id=item_id).first()
        if not item:
            return jsonify({'error': 'Bucketlist item not found!'})
        else:
            item.delete()
            return jsonify({'message': 'Bucketlist item deleted'})

    # @app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
    # @token_required


    return app
