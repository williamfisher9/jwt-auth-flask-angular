from src.extensions.extensions import db
from src.model.user_roles import UserRoles

class User(db.Model):
    __tablename__:str = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_img_name = db.Column(db.String(100), nullable=True)

    roles = db.relationship("Role", secondary=UserRoles.__table__, back_populates="users")

    def __init__(self, username:str, first_name:str, last_name:str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __repr__(self):
        return f'<User {self.username}>'


    def __str__(self):
        return f'User {self.username} {self.first_name} {self.last_name}'

    def to_dict(self):
        roles = []
        for role in self.roles:
            roles.append(role.to_dict())
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "profile_img_name": self.profile_img_name,
            "roles": roles
        }