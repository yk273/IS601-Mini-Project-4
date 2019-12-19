# /src/views/UserView

from flask import request, json, Response, Blueprint
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def create():
    """
    Create User Function
    """
    #####################
    # existing code remain #
    ######################

    return custom_response({'jwt_token': token}, 201)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))

    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)

    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    ser_data = user_schema.dump(user).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)

    #####################
    # existing code remain #
    ######################