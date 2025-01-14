from flask import Blueprint, jsonify, request
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from sqlalchemy.exc import IntegrityError

from src.messages.response_message import ResponseMessage
from src.model.user import User
from src.model.role import Role
from src.extensions.extensions import bcrypt, db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from src.configs.json_schemas import user_register_request_schema, user_login_request_schema

users_blueprint = Blueprint("users_blueprint", __name__)

@users_blueprint.route("/api/v1/users", methods=['GET'])
@jwt_required()
def get_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify(users=[user.to_dict() for user in users]), 200

@users_blueprint.route("/api/v1/users/register", methods=['POST'])
def create_user():
    if request.method == 'POST':
        request_json = request.get_json()

        try:
            validate(instance=request_json, schema=user_register_request_schema)
        except ValidationError as e:
            response_message = ResponseMessage(e.message, 400).create_response_message()
            return response_message, response_message['status']
        except Exception as e:
            response_message = ResponseMessage(e.__repr__(), 400).create_response_message()
            return response_message, response_message['status']

        user = User(request_json["username"],
                    request_json["first_name"],
                    request_json["last_name"])

        user.password = bcrypt.generate_password_hash(request_json["password"])

        roles = []
        for role in request_json["roles"]:
            role_in = Role.query.filter_by(name=role).first()
            roles.append(role_in)

        user.roles.extend(roles)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            response_message = ResponseMessage(f'{type(e).__name__}: username exists in the system', 409).create_response_message()
            return response_message, response_message['status']
        except Exception as e:
            response_message = ResponseMessage(e.__repr__(), 400).create_response_message()
            return response_message, response_message['status']

        response_message = ResponseMessage(user, 201).create_response_message()
        return response_message, response_message['status']

@users_blueprint.route("/api/v1/users/login", methods=['POST'])
def login_user():
    if request.method == 'POST':
        request_json = request.get_json()

        try:
            validate(instance=request_json, schema=user_login_request_schema)
        except ValidationError as e:
            response_message = ResponseMessage(e.message, 400).create_response_message()
            return response_message, response_message['status']
        except Exception as e:
            response_message = ResponseMessage(e.__repr__(), 400).create_response_message()
            return response_message, response_message['status']

        user = User.query.filter_by(username=request_json['username']).first()

        if not user:
            response_message = ResponseMessage("user was not found", 404).create_response_message()
            return response_message, response_message['status']

        if not bcrypt.check_password_hash(user.password, request_json['password']):
            response_message = ResponseMessage("invalid username/password", 403).create_response_message()
            return response_message, response_message['status']

        token = create_access_token(identity=user.username)

        response_message = ResponseMessage(token, 200).create_response_message()
        return response_message, response_message['status']