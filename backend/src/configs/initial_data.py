import mysql.connector
from src.extensions.extensions import db
from src.model.role import Role
from src.model.menu_items import Menu


def initialize_database():
    my_db_connection = mysql.connector.connect(user='root',
                                               password='root123',
                                               port="3306",
                                               host='localhost')

    my_cursor = my_db_connection.cursor()

    my_cursor.execute("DROP DATABASE users_jwt")
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS users_jwt")

    """
    my_cursor.execute("show databases")
    for db in my_cursor:
        print(db)
    """

    my_db_connection.close()

    db.create_all()

    roles = Role.query.all()
    if not roles:
        role1 = Role(name="ADMIN_ROLE")
        role2 = Role(name="USER_ROLE")
        db.session.add_all([role1, role2])
        db.session.commit()

    menu_items = Menu.query.all()
    if not menu_items:
        menu_item_1 = Menu("login", "fa-arrow-right-to-bracket", "/login", "public")
        menu_item_2 = Menu("register", "fa-user-plus", "/register", "public")
        menu_item_3 = Menu("home", "fa-home", "/user-home", "USER_ROLE")
        menu_item_4 = Menu("users", "fa-users", "/settings", "USER_ROLE")
        menu_item_5 = Menu("logout", "fa-right-from-bracket", "/logout", "USER_ROLE")
        db.session.add_all([menu_item_1, menu_item_2, menu_item_3, menu_item_4, menu_item_5])
        db.session.commit()
