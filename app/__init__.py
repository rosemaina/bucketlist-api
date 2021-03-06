"""This module contains all endpoints"""
# Importing objects from flask
import os
import jwt
import datetime

from flask import request, jsonify, render_template
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
    app.url_map.strict_slashes = False
    # loads up config settings
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Connects to the db
    db.init_app(app)

    from app.models import User
    from app.models import Bucketlist
    from app.models import Item

    @app.route('/')
    def index():
        """This method returns a Home Page"""
        return render_template("index.html")

    def token_required(f):
        """This valids token"""
        # This takes in a function f
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            # Checks if auth is in the header
            if 'Authorization' in request.headers:
                # Reads token value
                token = request.headers['Authorization']

            if not token:
                # Returns an error if token is missing
                return jsonify(
                    {'error': 'Invalid token. Please register or login'}), 401
            try:
                # Trying to decode the token found using the secret key
                id = jwt.decode(token, os.getenv('SECRET'))['id']
                current_user = User.query.filter_by(id=id).first()
                if not current_user:
                    return jsonify({'message': 'user not found!'}), 404
            except:
                return jsonify({'message': 'Expired token! Please login'}), 401

            # Returns the function with the user accessing the token
            return f(current_user=current_user, *args, **kwargs)

        return decorated

    @app.route('/auth/register/', methods=['POST'])
    def user_registration():
        """Method registers a user"""
        email = request.data['email']
        password = request.data['password']
        try:
            reg_user = User.query.filter_by(email=email).first()
            if reg_user:
                resp = jsonify({'message': 'Email address already exists!'})
                resp.status_code = 409
                return resp
            if email and password:
                if len(password.strip(" ")) >= 8:
                    striped_password = password.strip(" ")
                    if User.validate_email(email):
                        new_user = User(email)
                        new_user.create_password(striped_password)
                        new_user.save()
                        resp = jsonify(
                            {'message': 'Successful registration!'})
                        resp.status_code = 201
                        return resp
                    else:
                        resp = jsonify(
                            {'message': 'Invalid email address!'})
                        resp.status_code = 403
                        return resp
                else:
                    # Takes the text and turns it into a json
                    return jsonify(
                        {'message': 'Password length is too short!'}), 411
            else:
                return jsonify(
                    {'message': 'Email and password required!'}), 400
        except:
            return jsonify({'error': 'An error occured!'}), 500

    @app.route('/auth/login/', methods=['POST'])
    def user_login():
        email = request.data['email']
        password = request.data['password']
        found_user = User.query.filter_by(email=email).first()
        if not found_user:
            return jsonify({'error': 'User not found'}), 401

        if not found_user.validate_password(password):
            resp = jsonify({'error': 'Wrong password!'})
            resp.status_code = 401
            return resp
        resp = found_user.gen_token()
        resp.status_code = 200
        return resp

    @app.route('/auth/logout/', methods=['POST'])
    @token_required
    def logout(current_user):
        """Method logs out user"""
        token = jwt.encode({
            'id': current_user.id,
            'exp': datetime.datetime.utcnow()
        }, os.getenv('SECRET'))
        return jsonify({'token': token.decode('UTF-8')})

    @app.route('/auth/reset_password/', methods=['POST'])
    def reset_password():
        email = request.data['email']
        new_password = request.data['password']
        found_user = User.query.filter_by(email=email).first()

        if found_user:
            found_user.create_password(new_password)
            found_user.save()
            return jsonify(
                {'message': 'Password has changed successfully'}), 200
        return jsonify({'error': 'User not found!'}), 404

    @app.route('/auth/delete/', methods=['DELETE'])
    @token_required
    def delete_user(current_user):
        password = str(request.data.get('password'))
        found_user = User.query.filter_by(id=current_user.id).first()
        if not found_user:
            return jsonify({'error': 'User not found'}), 404
        else:
            if password:
                if found_user.validate_password(password):
                    found_user.delete()
                    return jsonify({'message': 'User is deleted'}), 200
                return jsonify({'error': 'Please input correct password'}), 405
            return jsonify({'error': 'Please input your password'}), 405

    # CRUD BU
    @app.route('/bucketlist/', methods=['POST', 'GET'])
    @token_required
    def create_bucketlist(current_user):

        title = str(request.data.get('title'))
        user_id = current_user.id
        if request.method == "POST":
            if title.strip(' '):
                striped_title = title.strip(" ")
                bucketlist = Bucketlist.query.filter_by(
                    user_id=current_user.id, title=striped_title).first()
                # Create and saves the striped title
                if not bucketlist:
                    new_bucket = Bucketlist(
                        title=striped_title, user_id=user_id)
                    new_bucket.save()
                    resp = jsonify({
                        'id': new_bucket.id,
                        'title': new_bucket.title,
                        'date_created': new_bucket.date_created,
                        'date_modified': new_bucket.date_modified
                    })
                    resp.status_code = 201
                    return resp
                return jsonify({'error': 'Title already taken!'}), 403
            return jsonify(
                {'error': 'Blank title. Please write your title'}), 401
        else:
            # GETs all bucketlists
            url_endpoint = '/bucketlist/'
            search = request.args.get('q')
            page = int(request.args.get('page', default=1))
            # The page content limit should be 10
            try:
                limit = int(request.args.get('limit', default=10))
            except ValueError:
                return jsonify({'error': 'Error, pass a number'}), 406

            # Searches a bucketlist using q
            if search:
                found_bucket = Bucketlist.query.filter_by(
                    user_id=user_id).filter(Bucketlist.title.like(
                        '%'+search+'%')).paginate(page, limit, False)
            else:
                found_bucket = Bucketlist.query.filter_by(
                    user_id=user_id).paginate(page, limit, False)
            if not found_bucket.items:
                return jsonify({'error': 'Bucketlists not found'}), 404

            bucket_dict = {"bucketlist": []}
            next_page = found_bucket.has_next if found_bucket.has_next else ''
            prev_page = found_bucket.has_prev if found_bucket.has_prev else ''
            # Base URl, concancate the pages,update page, give it a limit
            if next_page:
                next_page = url_endpoint + '?page=' + str(
                    page + 1) + '&limit=' + str(limit)
            else:
                next_page = ''

            if prev_page:
                prev_page = url_endpoint + '?page=' + str(
                    page - 1) + '&limit=' + str(limit)
            else:
                prev_page = ''

            for bucket in found_bucket.items:
                obj = {
                    'id': bucket.id,
                    'title': bucket.title,
                    'date_created': bucket.date_created,
                    'date_modified': bucket.date_modified
                }
                bucket_dict["bucketlist"].append(obj)
            bucket_dict['next_page'] = next_page
            bucket_dict['prev_page'] = prev_page
            return jsonify(bucket_dict), 200

    @app.route('/bucketlist/<id>/', methods=['GET'])
    @token_required
    def get_bucket(current_user, id):
        """Retrieves a buckelist using it's ID"""
        bucketlist = Bucketlist.query.filter_by(
            user_id=current_user.id, id=id).first()
        if not bucketlist:
            return jsonify({'error': 'Bucketlist Not found'}), 403
        else:
            resp = {
                'id': bucketlist.id,
                'title': bucketlist.title,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
            }
            return jsonify(resp), 200

    @app.route('/bucketlist/<id>/', methods=['DELETE'])
    @token_required
    def delete_bucket(current_user, id):
        """Deleting a specific bucketlist"""
        # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(
            user_id=current_user.id, id=id).first()
        if not bucketlist:
            return jsonify({'error': 'Bucketlist Not found'}), 404
        else:
            title = bucketlist.title
            bucketlist.delete()
            return jsonify(
                {'message': 'Bucketlist {} deleted'.format(title)}), 200

    @app.route('/bucketlist/<id>/', methods=['PUT'])
    @token_required
    def edit_bucket(current_user, id):
        """Edits a bucketlist"""
        title = str(request.data.get('title'))
        bucketlist = Bucketlist.query.filter_by(
            user_id=current_user.id, id=id).first()
        if not bucketlist:
            return jsonify({'message': 'Bucketlist NOT found'}), 403
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

    # CRUD BUCKET LIST ITEMS
    @app.route('/bucketlist/<id>/item/', methods=['POST'])
    @token_required
    def create_item(current_user, id):
        """Method creates an item"""
        name = request.data['name']
        bucket_id = id
        found_bucket = Bucketlist.query.filter_by(
            user_id=current_user.id, id=bucket_id).first()
        if found_bucket:
            if request.method == "POST":
                if name.strip(' '):
                    striped_name = name.strip(" ")
                    item = Item.query.filter_by(
                        bucket_id=id, name=striped_name).first()
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
                return jsonify({'error': 'Item name not given!'}), 401
        return jsonify({'error': 'Bucketlist does not exist!'}), 403

    @app.route('/bucketlist/<id>/item/<item_id>/', methods=['DELETE'])
    @token_required
    def delete_bucketlist_item(current_user, id, item_id):
        """"Deltes a bucketlist"""
        item = Item.query.filter_by(bucket_id=id, id=item_id).first()
        if not item:
            return jsonify({'error': 'Bucketlist item not found!'}), 403
        else:
            item.delete()
            return jsonify({'message': 'Bucketlist item deleted'})

    @app.route('/bucketlist/<id>/item/<item_id>/', methods=['PUT'])
    @token_required
    def edit_bucketlist_item(current_user, id, item_id):
        """Edits a bucketlist"""
        found_bucket = Bucketlist.query.filter_by(
            user_id=current_user.id, id=id).first()
        if found_bucket:
            name = str(request.data.get('name'))
            item = Item.query.filter_by(id=item_id, bucket_id=id).first()
            if not item:
                return jsonify({'message': 'Bucketlist item Not found'}), 403
            else:
                item.name = name
                item.save()
                resp = {
                    'id': item.id,
                    'name': item.name
                }
                return jsonify(resp), 200
        return jsonify({'error': 'User does not own that bucketlist!'})

    return app
