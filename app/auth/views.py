from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort

from app.models import User, BucketList, BucketlistItems


class RegistrationView(MethodView):
    """Create a new user"""

    def post(self):
        """handle post requests for this view. URL: /auth.register/"""

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            try:
                post_data = request.data
                username = post_data['username']
                email = post_data['email']
                password = post_data['password']
                user = User(username=username, email=email, password=password)
                user.save()

                response = {
                    "message": "You have registered successfully"
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    "message": str(e)
                }
        else:
            response = {
                "message": "User already exists"
            }
            return make_response(jsonify(response)), 409


class LoginView(MethodView):
    """Handles user login and access token generation"""

    def post(self):
        """Handles the POST request for this view. URL: /auth/login/"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response))
            else:
                response = {
                    'message': 'Invalid email or password. Try again please.'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


class BucketlistView(MethodView):
    """Handles bucketlist creation and manipulation"""

    def post(self):
        """Handles POST request for a new bucketlist"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    name = request.data.get('name', '')
                    bucketlist = BucketList(name=name, created_by=user_id)
                    bucketlist.save()
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': user_id
                    })

                    return make_response(response), 201
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def delete(self, id, **kwargs):
        """Handles DELETE request to delete a bucketlist"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    bucketlist = BucketList.query.filter_by(id=id).first()
                    if not bucketlist:
                        abort(404)
                    else:
                        bucketlist.delete()
                    return{"message":
                           "bucketlist {} successfully deleted".format(
                               bucketlist.id)}, 200
                    # raise HTTP 404 response if id not found
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def put(self, id, **kwargs):
        """Handles the PUT request to edit bucketlist"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    bucketlist = BucketList.query.filter_by(id=id).first()
                    if bucketlist:
                        name = str(request.data.get('name', ''))
                        bucketlist.name = name
                        bucketlist.save()
                        response = jsonify({
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                        })
                        return make_response(response), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def get(self, id, **kwargs):
        """Handles the GET request. Gets all the bucketlists"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    if id is None:
                        bucketlists = BucketList.query.filter_by(
                            created_by=user_id)
                        all_bucketlists = []
                        if bucketlists:
                            for bucketlist in bucketlists:
                                obj = {
                                    'id': bucketlist.id,
                                    'name': bucketlist.name,
                                    'date_created': bucketlist.date_created,
                                    'date_modified': bucketlist.date_modified,
                                    'created_by': bucketlist.created_by
                                }
                                all_bucketlists.append(obj)
                                response = jsonify(all_bucketlists)
                        else:
                            return{"message":
                                   "No existing bucketlist."}
                    # get the bucketlist specified in url <int:id>
                    else:
                        bucketlist = BucketList.query.filter_by(
                            id=id, created_by=user_id).first()
                        if bucketlist:
                            response = jsonify({
                                'id': bucketlist.id,
                                'name': bucketlist.name,
                                'date_created': bucketlist.date_created,
                                'date_modified': bucketlist.date_modified,
                                'created_by': bucketlist.created_by
                            })
                    return make_response(response), 200
                    # raise HTTP 404 response if id not found
                else:
                    abort(404)
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404


class BucketlistItemView(MethodView):
    def get(self, bucketlist_id, id, **kwargs):
        """Handles the GET request. Gets all the bucketlists items or
        using item id"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    bucketlist = BucketList.query.filter_by(
                        id=bucketlist_id).first()
                    if bucketlist:
                        bucketlistitems = BucketlistItems.query.filter_by(
                            id=id).first()
                        response = jsonify({
                            'id': bucketlistitems.id,
                            'name': bucketlistitems.name,
                            'date_created': bucketlistitems.date_created,
                            'date_modified': bucketlistitems.date_modified,
                            'done': bucketlistitems.done,
                            'bucketlist_id': bucketlistitems.bucketlist_id
                        })
                        return make_response(response), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404

    def post(self, bucketlist_id, **kwargs):
        """Handles POST requests for bucketlist id"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    bucketlist = BucketList.query.filter_by(
                        id=bucketlist_id).first()
                    if bucketlist:
                        name = request.data.get('name', '')
                        done = request.data.get('done', '')
                        bucketlistitem = BucketlistItems(
                            name=name, done=done, bucketlist_id=bucketlist_id)
                        bucketlistitem.save()

                        response = jsonify({
                            'id': bucketlistitem.id,
                            'name': bucketlistitem.name,
                            'date_created': bucketlistitem.date_created,
                            'date_modified': bucketlistitem.date_modified,
                            'done': bucketlistitem.done,
                            'bucketlist_id': bucketlistitem.bucketlist_id
                        })

                        return make_response(response), 201

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response))

    def put(self, id, bucketlist_id, **kwargs):
        """Handles PUT request to edit an item"""
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):
                    bucketlist = BucketList.query.filter_by(
                        id=bucketlist_id).first()
                    if bucketlist:
                        bucketlistitem = BucketlistItems.query.filter_by(
                            id=id).first()
                        if bucketlistitem:
                            name = request.data.get('name', '')
                            done = request.data.get('done', '')
                            bucketlistitem = BucketlistItems(
                                name=name, done=done,
                                bucketlist_id=bucketlist_id)
                            bucketlistitem.save()
                            response = jsonify({
                                'id': bucketlistitem.id,
                                'name': bucketlistitem.name,
                                'date_created': bucketlistitem.date_created,
                                'date_modified': bucketlistitem.date_modified,
                                'done': bucketlistitem.done,
                                'bucketlist_id': bucketlistitem.bucketlist_id
                            })

                            return make_response(response), 201
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response))


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
bucketlist_view = BucketlistView.as_view('bucketlist_view')
bucketlistitem_view = BucketlistItemView.as_view('bucketlistitem_view')


auth_blueprint.add_url_rule(
    '/auth/register/',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login/',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/bucketlists/',
    view_func=bucketlist_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/bucketlists/',
    defaults={'id': None},
    view_func=bucketlist_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/bucketlists/<int:id>',
    view_func=bucketlist_view,
    methods=['DELETE', 'PUT', 'GET']
)
auth_blueprint.add_url_rule(
    '/bucketlists/<int:bucketlist_id>/items/<int:id>',
    view_func=bucketlistitem_view,
    methods=['DELETE', 'PUT', 'GET']
)
auth_blueprint.add_url_rule(
    '/bucketlists/<int:bucketlist_id>/items/',
    view_func=bucketlistitem_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/bucketlists/<int:bucketlist_id>/items/',
    defaults={'id': None},
    view_func=bucketlistitem_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/bucketlists/<int:bucketlist_id>/items/<int:id>',
    view_func=bucketlistitem_view,
    methods=['PUT', 'GET']
)
