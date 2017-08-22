"""This module contains all endpoints"""
# Importing objects from flask
from flask import request, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
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
            return 'User ' + email + ' not found'
        if found_user.validate_password(password):
            resp = jsonify({'message': 'You are logged in'})
            resp.status_code = 200
            return resp

    # @app.route('/auth/logout', methods=['POST'])
    # def logout():
    #     email = request.data['email']
    #     password = request.data['password']


    # @app.route('/auth/reset-password', methods=['POST'])

    # # CRUD bucketlist
    @app.route('/bucketlist', methods=['POST', 'GET'])
    def create_bucketlist():
        if request.method == "POST":
            title = str(request.data.get('title'))
            user_id = str(request.data.get('user_id'))

            if title:
                bucketlist = Bucketlist(title=title, user_id=user_id)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            bucketlists = Bucketlist.get_all(user_id)
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'title': bucketlist.title,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            print(response)
            return response


    # @app.route('/bucketlists/<id>', methods=['GET'])

    # @app.route('/bucketlists/<id>', methods=['PUT'])

    # @app.route('/bucketlists/<id>', methods=['DELETE'])

    # # CRUD bucket items
    # @app.route('/bucketlists/<id>/items/', methods['POST'])

    # @app.route('/bucketlists/<id>/items/<item_id>', methods['PUT'])

    # @app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])

    return app
