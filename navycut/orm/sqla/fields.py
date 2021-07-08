from sqlalchemy import (Column as ColumnType, 
                    String as StringType, 
                    Integer as IntegerType,
                    BigInteger as BigIntegerType,
                    SmallInteger as SmallIntegerType,
                    Float as FloatType,
                    Text as TextType,
                    Boolean as BooleanType,
                    LargeBinary as LargeBinaryType,
                    Date as DateType,
                    Time as TimeType,
                    ForeignKey as ForeignKeyType,
                    DateTime as DateTimeType, 
                    Table as TableType
                    )
from sqlalchemy.orm import (relationship, 
                    backref as backref_func
                    )
from sqlalchemy_jsonfield import JSONField as JSONType
from flask_sqlalchemy.model import camel_to_snake_case
from .types import ImageType
from .meta import meta
from datetime import datetime

class Column(ColumnType):

    def __init__(self, *wargs, **kwargs):

        if "choices" in kwargs: 
            self.choices = kwargs.pop("choices")

        if "help_text" in kwargs:
            self.help_text = kwargs.pop("help_text")

        if "widget" in kwargs:
            self.widget = kwargs.pop("widget", None)

        return super(Column, self).__init__(*wargs, **kwargs)

class Fields:
    """
    The default field class for sqlalchemy object.
    """
    @classmethod
    def Text(cls, required:bool=False,
            unique:bool=False,
            help_text:str=None,
            widget:str="ckeditor") -> Column:

        """
        The Text fields for sqlalchemy,
        
        :param required:
            If False, the field is allowed to be blank. Default is False.


        :param unique:
            If True, this field must be unique throughout the table.

        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :param wdiget:
            Declare the text widget are box for admin section.
            Default is "ckeditor".
            available options - "ckeditor", "tinymce"

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Text(required=True, widget="ckeditor")
        """

        return Column(
            TextType,
            nullable=True if not required else False,
            unique=unique,
            help_text=help_text,
            widget=widget
        )

    @classmethod
    def Char(cls, max_length:int=255, 
            required:bool=False, 
            pk:bool=False, 
            unique:bool=False, 
            choices:tuple=None,
            help_text:str=None) -> Column:
        
        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        :param max_length:
            the maximum length of the field. only applicable for Cahr field.
            Default value is 255.
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param pk:
            If True, this field is the primary key for the model.

        :param unique:
            If True, this field must be unique throughout the table.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Char(max_length=255, unique=True)
        """

        # returning the sqlalchemy Column 
        # object with proper validations.

        return Column(
                StringType(max_length), 
                nullable=True if not required else False, 
                unique=unique, 
                choices = choices,
                help_text=help_text,
                primary_key=pk)

    @classmethod
    def Float(cls, required:bool=False,
            pk:bool=False,
            unique:bool=False,
            choices:tuple=None,
            help_text:str=None) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param pk:
            If True, this field is the primary key for the model.

        :param unique:
            If True, this field must be unique throughout the table.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Float(required=True)
        """

        return Column(
            FloatType,
            primary_key=pk,
            nullable=True if not required else False,
            unique = unique,
            choices=choices,
            help_text=help_text 
        )

    @classmethod
    def Integer(cls, required:bool=False,
                pk:bool=True,
                unique:bool=False,
                choices:tuple=None,
                help_text:str=None) -> Column:
        
        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param pk:
            If True, this field is the primary key for the model.

        :param unique:
            If True, this field must be unique throughout the table.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Integer(required=True)
        """

        return Column(
            IntegerType,
            primary_key=pk,
            nullable=True if not required else False,
            unique=unique,
            choices=choices,
            help_text=help_text
        )

    @classmethod
    def BigInteger(cls, required:bool=False,
                pk:bool=False,
                unique:bool=False,
                choices:tuple=None,
                help_text:str=None) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param pk:
            If True, this field is the primary key for the model.

        :param unique:
            If True, this field must be unique throughout the table.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.BigInteger(required=True)
        """

        return Column(
            BigIntegerType,
            nullable= True if not required else False,
            unique = unique,
            primary_key=pk,
            choices=choices,
            help_text=help_text
        )

    @classmethod
    def SmallInteger(cls, required:bool=False,
                pk:bool=False,
                unique:bool=False,
                choices:tuple=None,
                help_text:str=None) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param pk:
            If True, this field is the primary key for the model.

        :param unique:
            If True, this field must be unique throughout the table.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.SmallInteger(required=True)
        """

        return Column(
            SmallIntegerType,
            nullable= True if not required else False,
            unique = unique,
            primary_key=pk,
            choices=choices,
            help_text=help_text
        )

    @classmethod
    def Boolean(required:bool=False,
            default:bool=None,
            help_text:str=None,
            unique=False) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.

        :param unique:
            If True, this field must be unique throughout the table.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Boolean(required=True)
        """

        return Column(
            BooleanType,
            nullable=True if not required else False,
            unique=unique,
            help_text=help_text,
            default=default
        )
    
    @classmethod
    def Json(cls, required:bool=False,
            default:dict=dict(),
            help_text:str=None) -> Column:
        
        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.

        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Json(default={"name":"navycut", "planet":"Pluto"})
        """

        return Column(
            JSONType(enforce_string=True, enforce_unicode=False), 
            nullable= True if not required else False,
            default=default,
            help_text=help_text
            )

    @classmethod
    def Image(cls, required:bool=True,
            help_text:str = None
            ) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Image(required=True, help_text="insert the image here")
        """

        return Column(
                ImageType(255),
                nullable= True if not required else False,
                help_text=help_text
        )

    @classmethod
    def Binary(cls, required:bool=False,
            default:bytes=None,
            help_text:str=None) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.

        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.Binary(required=True)
        """

        return Column(
            LargeBinaryType,
            nullable=True if not required else False,
            default=default,
            help_text=help_text
        )

    @classmethod
    def LargeBinary(cls, required:bool=False,
            default:bytes=None,
            help_text:str=None) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            name = sql.fields.LargerBinary(requireed=True)
        """

        return Column(
            LargeBinaryType,
            nullable=True if not required else False,
            default=default,
            help_text=help_text
        )

    @classmethod
    def Time(cls, required:bool=False,
            default:datetime.time=None,
            help_text:str=None,
            choices:tuple=None
            ) -> Column:


        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            from datetime import datetime 
            name = sql.fields.Time(default=datetime.time)
        """

        return Column(
            TimeType,
            nullable=True if not required else False,
            help_text=help_text,
            default=default,
            choices=choices
        )

    @classmethod
    def Date(cls, required:bool=False,
            default:datetime.date=None,
            help_text:str=None,
            choices:tuple=None
            ) -> Column:

        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            from datetime import datetime
            name = sql.fields.Date(default=datetime.date)
        """

        return Column(
            DateType,
            nullable=True if not required else False,
            help_text=help_text,
            default=default,
            choices=choices
        )

    @classmethod
    def DateTime(cls, required:bool=False,
            default:datetime.now=None,
            help_text:str=None,
            choices:tuple=None
            ) -> Column:

        """
        The Datetime fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param default:
            Provide the default value for this column field.

        :param choices:
            A sequence consisting itself of iterables of exactly two items 
            (e.g. [(A, B), (A, B) ...]) to use as choices for this field. 
            If choices are given, they’re enforced by model validation and 
            the default form widget will be a select box with these choices 
            instead of the standard text field.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql
            from datetime import datetime
            name = sql.fields.DateTime(default=datetime.now)
        """

        return Column(
            DateTimeType,
            nullable=True if not required else False,
            help_text=help_text,
            default=default,
            choices=choices
        )

    #relationship field

    @classmethod
    def ForeignKey(cls, model:str,
                    unique:bool=False,
                    required:bool=False,
                    help_text:str=None) -> Column:

        """
        The ForiegnKey field for sqlalchemy,

        :param model: 
            Mention the name of the Model class here in str format only.
        
        :param required:
            If False, the field is allowed to be blank. Default is False.

        :param unique:
            If True, this field must be unique throughout the table.
        
        :param help_text:
            Extra “help” text to be displayed with the form widget. 
            It’s useful for documentation even if your field isn’t used on a form.

        :for example::

            from navycut.orm.sqla import sql

            class Blog(sql.Model):
                id = sql.fields.Integer(pk=True, unique=True)
                heading = sql.fields.Char(required=True, unique=True)
                author = sql.fields.OneToMany("Author")
            
            class Author(sql.Model):
                id = sql.fields.Integer(pk=True, unique=True)
                name = sql.fields.Char(required=True, unique=True)
                blog_id = sql.fields.ForiegnKey("Blog")
        """
        
        return Column(
            IntegerType,
            ForeignKeyType(f"{model.lower()}.id"),
            nullable=True if not required else False,
            unique=unique,
            help_text=help_text,
        )

    @classmethod
    def OneToOne(cls, 
                model:str, 
                backref:str,
                uselist:bool = False,
                ) -> Column:

        """
        The OneToOne relation for navycut orm.
        
        :param model: 
            Mention the name of the Model class here in str format only.

        :param backref: 
            Define the back reference for the relation.
            If no value, then it will default to provided model's name

        :for example::

            from navycut.orm.sqla import sql

            class Blog(sql.Model):
                id = sql.fields.Integer(pk=True, unique=True)
                heading = sql.fields.Char(required=True, unique=True)
                author = sql.fields.OneToOne("Author")
            
            class Author(sql.Model):
                id = sql.fields.Integer(pk=True, unique=True)
                name = sql.fields.Char(required=True, unique=True)
                blog_id = sql.fields.ForiegnKey("Blog", unique=True)
        """
        _table_name:str = camel_to_snake_case(model)
        
        return relationship(model, backref=backref_func(backref, uselist=False))

    @classmethod
    def ManyToOne(cls, 
                model:str, 
                backref:str,
                uselist:bool = True,
                ) -> Column:
        """
        The OneToMany relation for navycut orm.
        
        :param model: 
            Mention the name of the Model class here in str format only.

        :param backref: 
            Define the back reference for the relation.
            If no value, then it will default to provided model's name

        :for example::

            from navycut.orm.sqla import sql

            class Blog(sql.Model):
                id = sql.fields.Integer(pk=True, unique=True)
                heading = sql.fields.Char(required=True, unique=True)
                author = sql.fields.OneToMany("Author")
            
            class Author(sql.Model):
                id = sql.fields.Integer(pk=True, unique=True)
                name = sql.fields.Char(required=True, unique=True)
                blog_id = sql.fields.ForiegnKey("Blog")
        """

        return relationship(model, uselist=uselist, backref=backref)