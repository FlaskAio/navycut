from flask_login import UserMixin
from datetime import datetime
from navycut.orm import db
from navycut.utils.security import create_password_hash
from navycut.utils.logger import Console

# class Permission(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     type = db.Column(db.String(50), nullable=False, unique=True)


class Group(db.Model):
    """default group model for users."""
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)

group_user_con = db.Table("group_user_con", 
                    db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
                    db.Column('zone_id', db.Integer, db.ForeignKey("group.id"))
                    )

class User(db.Model, UserMixin):
    """
    The default user model.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, default=None, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    groups = db.relationship("Group", secondary=group_user_con, backref=db.backref("users", lazy='dynamic'))
    date_joined = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password:str):
        """
        change the password for the user.
        :param password: the new password for the user.
        """
        password_hash:str = create_password_hash(password)
        self.password = password_hash
        try: db.session.commit()
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
        db.session.add(grp)
    db.session.commit()
    Console.log.Success("initial data for admin privilage added successfully.")