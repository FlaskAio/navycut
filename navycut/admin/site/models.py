from flask_login import UserMixin
from datetime import datetime
from navycut.models import models
from navycut.utils.security import create_password_hash
from navycut.utils.logger import Console

# class Permission(models.Model):
#     id = models.Column(models.Integer, primary_key=True, unique=True, nullable=False)
#     type = models.Column(models.String(50), nullable=False, unique=True)


class Group(models.Model):
    """default group model for users."""
    id = models.Column(models.Integer, primary_key=True, unique=True, nullable=False)
    name = models.Column(models.String(255), nullable=False, unique=True)

group_user_con = models.Table("group_user_con", 
                    models.Column('user_id', models.Integer, models.ForeignKey("user.id")),
                    models.Column('zone_id', models.Integer, models.ForeignKey("group.id"))
                    )

class User(models.Model, UserMixin):
    """
    The default user model.
    """
    id = models.Column(models.Integer, primary_key=True, unique=True, nullable=False)
    first_name = models.Column(models.String(255), nullable=False)
    last_name = models.Column(models.String(255), nullable=True)
    email = models.Column(models.String(255), nullable=True)
    username = models.Column(models.String(255), nullable=False, unique=True)
    password = models.Column(models.String(100), nullable=False)
    is_staff = models.Column(models.Boolean, default=False)
    is_superuser = models.Column(models.Boolean, default=True)
    last_login = models.Column(models.DateTime, default=None, nullable=True)
    is_active = models.Column(models.Boolean, default=True)
    groups = models.relationship("Group", secondary=group_user_con, backref=models.backref("users", lazy='dynamic'))
    date_joined = models.Column(models.DateTime, default=datetime.now)

    def set_password(self, password:str):
        """
        change the password for the user.
        :param password: the new password for the user.
        """
        password_hash:str = create_password_hash(password)
        self.password = password_hash
        try: models.session.commit()
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
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<{self.first_name} {self.last_name}>"

def _insert_intial_data():
    #insert all the initial data to the equivalent table.
    available_groups = ['super_admin','admin', 'staff', 'customer']
    for group in available_groups:
        grp=Group(name=group)
        models.session.add(grp)
    models.session.commit()
    Console.log.Success("initial data for admin privilage added successfully.")