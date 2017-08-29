# import os
# import jwt

# from flask import  request, jsonify, abort


# @app.route('/auth/register', methods=['POST'])
# def user_registration():
#     """Method registers a user"""
#     email = request.data['email']
#     password = request.data['password']
#     try:
#         reg_user = User.query.filter_by(email=email).first()
#         if reg_user:
#             resp = jsonify({'message': 'Email address already exists!'})
#             resp.status_code = 409
#             return resp
#         if email and password:
#             if len(password.strip(" ")) >= 8:
#                 striped_password = password.strip(" ")
#                 if User.validate_email(email):
#                     new_user = User(email)
#                     new_user.create_password(striped_password)
#                     new_user.save()
#                     resp = jsonify(
#                         {'message': 'Successful registration!'})
#                     resp.status_code = 201
#                     return resp
#                 else:
#                     resp = jsonify(
#                         {'message': 'Invalid email address!'})
#                     resp.status_code = 403
#                     return resp
#             else:
#                 # Takes the text and turns it into a json
#                 return jsonify(
#                     {'message': 'Password length is too short!'}), 411
#         else:
#             return jsonify({'message': 'Email and password required!'}), 400
#     except:
#         resp = jsonify({'error': 'An error occured!'})
#         resp.status_code = 500
#         return resp

# @app.route('/auth/login', methods=['POST'])
# def user_login():
#     email = request.data['email']
#     password = request.data['password']
#     found_user = User.query.filter_by(email=email).first()
#     if not found_user:
#         resp = jsonify ({'error': 'User not found'})
#         resp.status_code = 401
#         return resp

#     if not found_user.validate_password(password):
#         resp = jsonify({'error': 'Wrong password!'})
#         resp.status_code = 401
#         return resp
#     resp = found_user.gen_token()
#     resp.status_code = 200
#     return resp

# @app.route('/auth/logout', methods=['POST'])
# def logout():
#     """Method logs out user"""
#     pass

# @app.route('/auth/reset_password', methods=['POST'])
# def reset_password():
#     email = request.data['email']
#     new_password = request.data['password']
#     found_user = User.query.filter_by(email=email).first()

#     if found_user:
#         found_user.create_password(new_password)
#         found_user.save()
#         return jsonify({'message': 'Password has changed successfully'}), 200
#     return jsonify({'error': 'User not found!'}), 403

# # CRUD BU
# @app.route('/bucketlist', methods=['POST', 'GET'])
# @token_required
# def create_bucketlist(current_user):

#     title = str(request.data.get('title'))
#     user_id = current_user.id
#     if request.method == "POST":
#         if title.strip(' '):
#             striped_title = title.strip(" ")
#             bucketlist = Bucketlist.query.filter_by(
#                 user_id=current_user.id, title=striped_title).first()
#             # Create and saves the striped title
#             if not bucketlist:
#                 new_bucket = Bucketlist(
#                     title=striped_title, user_id=user_id)
#                 new_bucket.save()
#                 resp = jsonify({
#                     'id': new_bucket.id,
#                     'title': new_bucket.title,
#                     'date_created': new_bucket.date_created,
#                     'date_modified': new_bucket.date_modified
#                 })
#                 resp.status_code = 201
#                 return resp
#             return jsonify({'error': 'Title already taken!'}), 403
#         return jsonify({'error': 'Blank title. Please write your title'}), 401
#     else:
#         # GETs all bucketlists
#         bucketlists = Bucketlist.query.filter_by(user_id=user_id).all()
#         if not bucketlists:
#             return jsonify({'error': 'No bucketlists found!'}), 403

#         results = []
#         for bucketlist in bucketlists:
#             obj = {
#                 'id': bucketlist.id,
#                 'title': bucketlist.title,
#                 'date_created': bucketlist.date_created,
#                 'date_modified': bucketlist.date_modified
#             }
#             results.append(obj)
#         resp = jsonify(results)
#         resp.status_code = 200
#         return resp

# @app.route('/bucketlist/<id>', methods=['GET'])
# @token_required
# def get_bucket(current_user, id):
#     """Retrieves a buckelist using it's ID"""
#     bucketlist = Bucketlist.query.filter_by(
#         user_id=current_user.id, id=id).first()
#     if not bucketlist:
#         return jsonify({'error': 'Bucketlist Not found'}), 403
#     else:
#         # print(bucketlist.items)
#         # bucketlist_items = Item.query.filter_by(bucket_id=id)
#         # query all bucketlist items with the bucket id
#         resp = {
#             'id': bucketlist.id,
#             'title': bucketlist.title,
#             'date_created': bucketlist.date_created,
#             'date_modified': bucketlist.date_modified,
#             # 'items': { items }
#         }
#         return jsonify(resp), 200

# @app.route('/bucketlist/<id>', methods=['DELETE'])
# @token_required
# def delete_bucket(current_user, id):
#     """Deleting a specific bucketlist"""
#     # retrieve a buckelist using it's ID
#     bucketlist = Bucketlist.query.filter_by(
#         user_id=current_user.id, id=id).first()
#     if not bucketlist:
#         return jsonify({'error': 'Bucketlist Not found'}), 403
#     else:
#         title = bucketlist.title
#         bucketlist.delete()
#         return jsonify({'message': 'Bucketlist {} deleted'.format(title)}), 200

# @app.route('/bucketlist/<id>', methods=['PUT'])
# @token_required
# def edit_bucket(current_user, id):
#     """Edits a bucketlist"""
#     title = str(request.data.get('title'))
#     bucketlist = Bucketlist.query.filter_by(
#         user_id=current_user.id, id=id).first()
#     if not bucketlist:
#         return jsonify({'message': 'Bucketlist NOT found'}), 403
#     else:
#         bucketlist.title = title
#         bucketlist.save()
#         resp = {
#             'id': bucketlist.id,
#             'title': bucketlist.title,
#             'date_created': bucketlist.date_created,
#             'date_modified': bucketlist.date_modified
#         }
#         return jsonify(resp), 200

# # CRUD BUCKET LIST ITEMS
# @app.route('/bucketlist/<id>/item', methods=['POST'])
# @token_required
# def create_item(current_user, id):
#     """Method creates an item"""
#     name = request.data['name']
#     bucket_id = id
#     found_bucket = Bucketlist.query.filter_by(
#         user_id=current_user.id, id=bucket_id).first()
#     if found_bucket:
#         if request.method == "POST":
#             if name.strip(' '):
#                 striped_name = name.strip(" ")
#                 item = Item.query.filter_by(
#                     bucket_id=id, name=striped_name).first()
#                 if not item:
#                     new_item = Item(name=striped_name, bucket_id=bucket_id)
#                     new_item.save()
#                     resp = jsonify({
#                         'id': new_item.id,
#                         'name': new_item.name,
#                     })
#                     resp.status_code = 201
#                     return resp
#                 return jsonify({'error': 'Name already exists'}), 403
#             return jsonify({'error': 'Item name not given!'}), 401
#     return jsonify({'error':'Bucketlist does not exist!'}), 403
#     # else:
#     #     # GETs all items in a list
#     #     items = Item.query.filter_by(bucket_id=id).all()
#     #     if not items:
#     #         return jsonify({'error': 'No bucket items found!'}), 403

#     #     results = []
#     #     for item in items:
#     #         obj = {
#     #             'id': item.id,
#     #             'name': item.name
#     #         }
#     #         results.append(obj)
#     #     resp = jsonify(results)
#     #     resp.status_code = 200
#     #     return resp

# @app.route('/bucketlist/<id>/item/<item_id>', methods=['DELETE'])
# @token_required
# def delete_bucketlist_item(current_user, id, item_id):
#     """"Deltes a bucketlist"""
#     item = Item.query.filter_by(bucket_id=id, id=item_id).first()
#     if not item:
#         return jsonify({'error': 'Bucketlist item not found!'}), 403
#     else:
#         item.delete()
#         return jsonify({'message': 'Bucketlist item deleted'})

# @app.route('/bucketlist/<id>/item/<item_id>', methods=['PUT'])
# @token_required
# def edit_bucketlist_item(current_user, id, item_id):
#     """Edits a bucketlist"""
#     found_bucket = Bucketlist.query.filter_by(user_id=current_user.id, id=id).first()
#     if found_bucket:
#         name = str(request.data.get('name'))
#         item = Item.query.filter_by(id=item_id, bucket_id=id).first()
#         if not item:
#             return jsonify({'message': 'Bucketlist item Not found'}), 403
#         else:
#             item.name = name
#             item.save()
#             resp = {
#                 'id': item.id,
#                 'name': item.name
#             }
#             return jsonify(resp), 200
#     return jsonify({'error': 'User does not own that bucketlist!'})
