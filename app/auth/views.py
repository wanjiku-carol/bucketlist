from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


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
            return make_response(jsonify(response)), 202


registration_view = RegistrationView.as_view('register_view')


auth_blueprint.add_url_rule(
    '/auth/register/',
    view_func=registration_view,
    methods=['POST']
)
