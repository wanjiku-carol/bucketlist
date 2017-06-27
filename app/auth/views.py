from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort

from app.models import User, BucketList, BucketlistItems
from app.auth.decorator import auth_token


class RegistrationView(MethodView):
    """Create a new user"""

    def post(self):
        """handle post requests for this view. URL: /auth.register/"""
        user = User.query.filter_by(email=request.data.get('email')).first()

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
            user = User.query.filter_by(email=request.data.get('email')).first()

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
    decorators = [auth_token]

    def post(self, **kwargs):
        """Handles POST request for a new bucketlist"""
        try:
            user_id = kwargs["user_id"]
            name = request.data.get('name', '')
            if name:
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
            else:
                response = {
                    "message": "Please enter a bucketlist name."
                }
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def delete(self, id, **kwargs):
        """Handles DELETE request to delete a bucketlist"""
        try:
            bucketlist = BucketList.query.filter_by(id=id).first()
            if not bucketlist:
                abort(404)
            else:
                bucketlist.delete()
                return{"message":
                       "bucketlist {} successfully deleted".format(
                           bucketlist.id)}, 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def put(self, id, **kwargs):
        """Handles the PUT request to edit bucketlist"""
        try:

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
            else:
                response = {
                    "message": "Bucketlist is Empty."
                }
                return make_response(jsonify(response))
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def get(self, id, **kwargs):
        """Handles the GET request. Gets all the bucketlists"""
        try:
            user_id = kwargs["user_id"]
            limit = request.args.get("limit", 20)
            page = request.args.get("page", 1)
            search_term = request.args.get("q", None)
            limit = 100 if int(limit) > 100 else int(limit)
            if search_term:
                bucketlists = BucketList.query.filter(
                    BucketList.name.ilike("%" + search_term + "%")).filter_by(
                    created_by=user_id)
            else:
                bucketlists = BucketList.query.filter_by(
                    created_by=user_id)
            if id is None:
                all_bucketlists = []
                if bucketlists:
                    bucketlists_pagination = bucketlists.paginate(
                        int(page), int(limit), False).items
                    for bucketlist in bucketlists_pagination:
                        obj = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                        }
                        all_bucketlists.append(obj)
                    response = jsonify(all_bucketlists)
                    return make_response(response), 200
                else:
                    return{"message":
                           "Bucketlist is Empty"}
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
                else:
                    response = {
                        "message": "Bucketist is empty"
                    }
                    return make_response(jsonify(response)), 404

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404


class BucketlistItemView(MethodView):

    decorators = [auth_token]

    def get(self, bucketlist_id, id, **kwargs):
        """Handles the GET request. Gets all the bucketlists items or
        using item id"""
        try:
            bucketlist = BucketList.query.filter_by(
                id=bucketlist_id).first()
            if bucketlist:
                if id:
                    bucketlistitems = BucketlistItems.query.filter_by(
                        id=id).first()
                    if bucketlistitems:
                        response = jsonify({
                            'id': bucketlistitems.id,
                            'name': bucketlistitems.name,
                            'date_created': bucketlistitems.date_created,
                            'date_modified': bucketlistitems.date_modified,
                            'done': bucketlistitems.done,
                            'bucketlist_id': bucketlistitems.bucketlist_id
                        })
                    else:
                        response = {
                            "message": "Item Not Found"
                        }
                        return make_response(jsonify(response))
                else:
                    all_items = []
                    bucketlistitems = BucketlistItems.query.all()
                    if bucketlistitems:
                        for item in bucketlistitems:
                            if item.bucketlist_id == bucketlist_id:
                                obj = {
                                    'id': item.id,
                                    'name': item.name,
                                    'date_created': item.date_created,
                                    'date_modified': item.date_modified,
                                    'done': item.done,
                                    'bucketlist_id': item.bucketlist_id
                                }
                                all_items.append(obj)
                                response = jsonify(all_items)
                    else:
                        return{"message":
                               "There are no items in bucketlist"}, 404
                return make_response(response), 200
            else:
                return{"message":
                       "Bucketlist is empty"}, 404
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404

    def post(self, bucketlist_id, **kwargs):
        """Handles POST requests for bucketlist id"""
        try:
            bucketlist = BucketList.query.filter_by(
                id=bucketlist_id).first()
            if bucketlist:
                name = request.data.get('name', '')
                done = request.data.get('done', '')
                if not done:
                    done = "False",
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
            else:
                response = {
                    "message": "Bucketlist is empty"
                }
                return make_response(jsonify(response))

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response))

    def put(self, id, bucketlist_id, **kwargs):
        """Handles PUT request to edit an item"""
        try:
            bucketlist = BucketList.query.filter_by(
                id=bucketlist_id).first()
            if bucketlist:
                bucketlistitem = BucketlistItems.query.filter_by(
                    id=id).first()
                if bucketlistitem:
                    name = request.data.get('name', '')
                    done = request.data.get('done', '')
                    bucketlistitem.name = name
                    bucketlistitem.done = done
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
                else:
                    response = {
                        "message": "Item does not exist"
                    }
                    return make_response(jsonify(response))
            else:
                response = {
                    "message": "Bucketlist is empty"
                }
                return make_response(jsonify(response))
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response))

    def delete(self, bucketlist_id, id, **kwargs):
        """Handles DELETE request to delete a bucketlist item"""
        try:
            bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
            if not bucketlist:
                abort(404)
            else:
                if id:
                    bucketlistitems = BucketlistItems.query.filter_by(
                        id=id).first()
                    if bucketlistitems:
                        bucketlistitems.delete()
                        return{"message":
                               "item {} successfully deleted".format(
                                   bucketlist.id)}, 200
                    else:
                        response = {
                            "message": "Item not found"
                        }
                        return make_response(jsonify(response))
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


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
    '/bucketlists/<int:id>/',
    view_func=bucketlist_view,
    methods=['DELETE', 'PUT', 'GET']
)
auth_blueprint.add_url_rule(
    '/bucketlists/<int:bucketlist_id>/items/<int:id>/',
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
    '/bucketlists/<int:bucketlist_id>/items/<int:id>/',
    view_func=bucketlistitem_view,
    methods=['PUT', 'GET']
)
