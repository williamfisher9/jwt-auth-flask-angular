from flask import Blueprint, jsonify, request
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

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
            return jsonify(message=e.message)
        except Exception as e:
            return jsonify(message=e.__repr__())

        user = User(request_json["username"],
                    request_json["first_name"],
                    request_json["last_name"])

        user.password = bcrypt.generate_password_hash(request_json["password"])

        roles = []
        for role in request_json["roles"]:
            role_in = Role.query.filter_by(name=role).first()
            roles.append(role_in)

        user.roles.extend(roles)

        db.session.add(user)
        db.session.commit()

        return jsonify(user=user.to_dict())

@users_blueprint.route("/api/v1/users/login", methods=['POST'])
def login_user():
    if request.method == 'POST':
        request_json = request.get_json()

        try:
            validate(instance=request_json, schema=user_login_request_schema)
        except ValidationError as e:
            return jsonify(message=e.message)
        except Exception as e:
            return jsonify(message=e.__repr__())

        user = User.query.filter_by(username=request_json['username']).first()

        if not user:
            return jsonify(message="user was not found"), 404

        if not bcrypt.check_password_hash(user.password, request_json['password']):
            return jsonify(message="invalid username/password"), 404

        token = create_access_token(identity=user.username)

        return jsonify(token=token), 200