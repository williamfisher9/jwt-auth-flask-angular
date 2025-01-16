import logging

from flask import Blueprint, jsonify, request, url_for, send_from_directory
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from src.messages.response_message import ResponseMessage
from src.model.menu_items import Menu
from src.model.user import User
from src.model.role import Role
from src.extensions.extensions import bcrypt, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from src.configs.json_schemas import user_register_request_schema, user_login_request_schema
import uuid
import os

users_blueprint = Blueprint("users_blueprint", __name__, url_prefix="/api/v1/users")

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_blueprint.route("get-menu-items", methods=['GET'])
@jwt_required(optional=True)
def get_menu_items():
    current_identity = get_jwt_identity()
    if current_identity:
        menu_items = Menu.query.filter_by(role_name="USER_ROLE").all()
        response_message = ResponseMessage(menu_items, 200).create_response_message()
        return response_message, response_message["status"]
    else:
        menu_items = Menu.query.filter_by(role_name="public").all()
        print(menu_items)
        response_message = ResponseMessage(menu_items, 200).create_response_message()
        return response_message, response_message["status"]

@users_blueprint.route("", methods=['GET'])
@jwt_required()
def get_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify(users=[user.to_dict() for user in users]), 200

@users_blueprint.route("/register", methods=['POST'])
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
            logger.error(e)
            response_message = ResponseMessage(f'{type(e).__name__}: username exists in the system', 409).create_response_message()
            return response_message, response_message['status']
        except Exception as e:
            response_message = ResponseMessage(e.__repr__(), 400).create_response_message()
            return response_message, response_message['status']

        response_message = ResponseMessage(user, 201).create_response_message()
        return response_message, response_message['status']

@users_blueprint.route("/login", methods=['POST'])
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

        response_message = ResponseMessage({"token": token, "user_id": user.id}, 200).create_response_message()
        return response_message, response_message['status']

@users_blueprint.route("/<id>", methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    user : User = User.query.filter_by(id=id).first()

    if not user:
        response_message = ResponseMessage("user was not found", 404).create_response_message()
        return response_message, response_message['status']

    user.profile_img_name = create_profile_image_url(user.profile_img_name)

    response_message = ResponseMessage(user, 200).create_response_message()
    return response_message, response_message['status']

@users_blueprint.route("/profile-image", methods=['POST'])
@jwt_required()
def update_user_profile_image():
    user : User = User.query.filter_by(id=request.values['id']).first()

    if not user:
        response_message = ResponseMessage("user was not found", 404).create_response_message()
        return response_message, response_message['status']

    if 'file' not in request.files:
        response_message = ResponseMessage("file not included in the request", 404).create_response_message()
        return response_message, response_message['status']

    file = request.files['file']

    if file.filename == '':
        response_message = ResponseMessage("improper file name", 404).create_response_message()
        return response_message, response_message['status']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_file_name = str(uuid.uuid1()) + "." + filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join("C://Users//william.fisher//Desktop//app_files//images", new_file_name))

        try:
            user.profile_img_name = new_file_name
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            response_message = ResponseMessage(e, 400).create_response_message()
            return response_message, response_message['status']

    response_message = ResponseMessage(create_profile_image_url(user.profile_img_name), 200).create_response_message()
    return response_message, response_message['status']

@users_blueprint.route('/get-user-profile-img/<filename>')
def get_user_profile_image(filename):
   return send_from_directory("C://Users//william.fisher//Desktop//app_files//images", filename, as_attachment=False)

def create_profile_image_url(filename):
    if filename:
        return url_for("users_blueprint.get_user_profile_image", _external=True, filename=filename)

