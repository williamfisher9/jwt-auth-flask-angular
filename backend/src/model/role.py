from enum import unique

from sqlalchemy import MetaData

from src.extensions.extensions import db
from src.model.user_roles import UserRoles


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    users = db.relationship("User", secondary=UserRoles.__table__, back_populates="roles")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'

    def __str__(self):
        return f'Role {self.name}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }