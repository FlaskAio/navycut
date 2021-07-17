from flask_login import UserMixin
from datetime import datetime
from navycut.orm import sql
from navycut.utils.security import create_password_hash
from navycut.utils.console import Console
import typing as t


# class Permission(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True, nullable=False)
#     type = sql.Column(sql.String(50), nullable=False, unique=True)


class Group(sql.Model):
    """
    default group model for users.
    """
    name = sql.fields.Char(required=True, unique=True)

    def __repr__(self) -> str:
        return self.name

group_user_con = sql.Table("group_user_con", 
                    sql.Column('user_id', sql.Integer, sql.ForeignKey("user.id")),
                    sql.Column('zone_id', sql.Integer, sql.ForeignKey("group.id"))
                    )

class User(sql.Model, UserMixin):
    """
    The default user model.
    """
    first_name = sql.Column(sql.String(255), nullable=False)
    last_name = sql.Column(sql.String(255), nullable=True)
    email = sql.Column(sql.String(255), nullable=True)
    username = sql.Column(sql.String(255), nullable=False, unique=True)
    password = sql.Column(sql.String(100), nullable=False)
    is_staff = sql.Column(sql.Boolean, default=False)
    is_superuser = sql.Column(sql.Boolean, default=True)
    last_login = sql.Column(sql.DateTime, default=None, nullable=True)
    is_active = sql.Column(sql.Boolean, default=True)
    groups = sql.relationship("Group", secondary=group_user_con, backref=sql.backref("users", lazy='dynamic'))
    date_joined = sql.Column(sql.DateTime, default=datetime.now)


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.password = create_password_hash(kwargs.pop('password'))
        self.save()

    def set_password(self, password:str):
        """UserMixin
        change the password for the user.
        :param password: the new password for the user.
        """
        password_hash:str = create_password_hash(password)
        self.password = password_hash
        self.save()

    def disable_user(self) -> bool:
        """
        to disable a particular user.
        """
        self.is_active = False
        self.save()
        return True

    def enable_user(self) -> bool:
        """
        to enable a particular user.
        """
        self.is_active = True
        self.save()
        return True

    @property
    def name(self) -> str:
        """
        return the name of the user.
        """
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __str__(self) -> str:
        """
        return the string representation of the user model object.
        """
        return self.name

    def __repr__(self) -> str:
        """
        return the representation of the user model object.
        """
        return self.name

def _insert_intial_data() -> None:
    #insert all the initial data to the equivalent table.
    available_groups = ['super_admin','admin', 'staff', 'customer']
    for group in available_groups:
        grp=Group(name=group)
        grp.save()
    Console.log.Success("initial data for admin privilage added successfully.")

def _get_user_by_username(username:str) -> t.Optional[User]:
    """
    get the user object if the entered username 
    present in the database or return None.

    :param username:
        provide the username. Default is the current username.
    """
    user:t.Optional[t.Type["User"]] = User.query.filter_by(username=username).first()
    
    return user