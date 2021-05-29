from flask_login import UserMixin
from datetime import datetime
from navycut.orm.sqla import sql
from navycut.utils.security import create_password_hash
from navycut.utils.console import Console

# class Permission(sql.Model):
#     id = sql.Column(sql.Integer, primary_key=True, unique=True, nullable=False)
#     type = sql.Column(sql.String(50), nullable=False, unique=True)


class Group(sql.Model):
    """default group model for users."""
    id = sql.Column(sql.Integer, primary_key=True, unique=True, nullable=False)
    name = sql.Column(sql.String(255), nullable=False, unique=True)

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
    id = sql.Column(sql.Integer, primary_key=True, unique=True, nullable=False)
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

    def set_password(self, password:str):
        """
        change the password for the user.
        :param password: the new password for the user.
        """
        password_hash:str = create_password_hash(password)
        self.password = password_hash
        try: sql.session.commit()
        except Exception: raise Exception

    def disable_user(self) -> bool:
        """
        to disable a particular user.
        """
        self.is_active = False
        return True

    @property
    def name(self) -> str:
        """
        return the name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        """return the string representation of the user model object."""
        return self.name

    def __repr__(self) -> str:
        return self.name

def _insert_intial_data():
    #insert all the initial data to the equivalent table.
    available_groups = ['super_admin','admin', 'staff', 'customer']
    for group in available_groups:
        grp=Group(name=group)
        grp.save()
    Console.log.Success("initial data for admin privilage added successfully.")