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


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule(
    '/auth/register/',
    view_func=registration_view,
    methods=['POST']
)
# Define the rule for the registration url
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login/',
    view_func=login_view,
    methods=['POST']
)
