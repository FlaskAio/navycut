from flask_login import UserMixin
from datetime import datetime
from navycut.orm import sql
from navycut.utils.security import create_password_hash
from nc_console import Console
import typing as t
from ..admin.site.views import NCAdminModelView


class Permission(sql.Model):
    name = sql.fields.Char(max_length=100, 
                        required=True, 
                        unique=True, 
                        help_text="The default name field for the permission model.")
    is_active = sql.fields.Boolean(default=True)
    created_at = sql.fields.DateTime(default=datetime.now())

    def __repr__(self) -> str:
        return f"<Permission '{self.name.capitalize()}'>"


group_perm_con = sql.Table("group_perm_con",
                sql.Column('perm_id', sql.Integer, sql.ForeignKey("permission.id")),
                sql.Column('group_id', sql.Integer, sql.ForeignKey("group.id"))
                )

class Group(sql.Model):
    """
    default group model for users.
    """
    name = sql.fields.Char(required=True, unique=True)
    permissions = sql.relationship("Permission", 
                secondary=group_perm_con, 
                backref=sql.backref("groups", lazy='dynamic'))
    created_at = sql.fields.DateTime(default=datetime.now())

    def __repr__(self) -> str:
        return f"<Group '{self.name.capitalize()}'>"

group_user_con = sql.Table("group_user_con", 
                    sql.Column('user_ptr_id', sql.Integer, sql.ForeignKey("user.id")),
                    sql.Column('group_ptr_id', sql.Integer, sql.ForeignKey("group.id"))
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
    """
    insert all the initial data to the equivalent table.
    """
    available_groups = ['super_admin','admin', 'staff', 'customer']
    available_perms = ['create', 'edit', 'delete']

    for group in available_groups:
        grp=Group(name=group)
        grp.save()

    grp:t.Type["Group"] = Group.query.filter_by(name='super_admin').first()
    for prm in available_perms:
        perm = Permission(name=prm)
        perm.save()
        grp.permissions.append(perm)
        grp.save()
    

    Console.log.Success("initial data for admin privilage added successfully.")

def _get_user_by_username(username:str) -> t.Optional[User]:
    """
    get the user object if the entered username 
    present in the database or return None.

    :param username:
        provide the username to get the User object or None.
    """
    user:t.Optional[t.Type["User"]] = User.query.filter_by(username=username).first()
    
    return user

class UsersCustomAdminView(NCAdminModelView):
    # edit_modal = True
    # form_overrides = dict(password=forms.FileField)
    # form_extra_fields = {
    #                 'gobinda': forms.FileField('Gobinda')
    #             }
    column_searchable_list = ["first_name", "username", "email"]