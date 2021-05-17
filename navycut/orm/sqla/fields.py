from sqlalchemy import (Column as ColumnType, 
                    String as StringType, 
                    Integer as IntegerType,
                    BigInteger as BigIntegerType,
                    SmallInteger as SmallIntegerType,
                    Float as FloatType,
                    Text as TextType,
                    Boolean as BooleanType,
                    LargeBinary as LargeBinaryType)
from sqlalchemy_jsonfield import JSONField as JSONType
from .types import ImageType

class Column(ColumnType):

    def __init__(self, *wargs, **kwargs):

        if "choices" in kwargs: 
            self.choices = kwargs.pop("choices")

        if "help_text" in kwargs:
            self.help_text = kwargs.pop("help_text")

        return super(Column, self).__init__(*wargs, **kwargs)

class Fields:
    """
    The default field class for sqlalchemy object.
    """
    def Text(self, required:bool=False,
            unique:bool=False,
            help_text:str=None) -> Column:

        return Column(
            TextType,
            nullable=True if not required else False,
            unique=unique,
        )


    def Char(self, max_length:int=255, 
            required:bool=False, 
            pk:bool=False, 
            unique:bool=False, 
            choices:list=None,
            help_text:str=None) -> Column:
        
        """
        The Charecter fields for sqlalchemy,
        if No maximum_length, it will seted to max_val.
        
        :param max_length:
            the maximum length of the field. only applicable for Cahr field.
            If None, then the default value will be the max value.
        
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

    def Float(self, required:bool=False,
            pk:bool=False,
            unique:bool=True,
            help_text:str=None) -> Column:

        return Column(
            FloatType,
            primary_key=pk,
            nullable=True if not required else False,
            unique = unique
        )

    def Integer(self, required:bool=False,
                pk:bool=True,
                unique:bool=False,
                help_text:str=None):
        
        return Column(
            IntegerType,
            primary_key=pk,
            nullable=True if not required else False,
            unique=unique
        )

    def BigInteger(self, required:bool=False,
                pk:bool=False,
                unique:bool=False,
                help_text:str=None) -> Column:

        return Column(
            BigIntegerType,
            nullable= True if not required else False,
            unique = unique,
            primary_key=pk
        )

    def SmallInteger(self, required:bool=False,
                pk:bool=False,
                unique:bool=False,
                help_text:str=None) -> Column:

        return Column(
            SmallIntegerType,
            nullable= True if not required else False,
            unique = unique,
            primary_key=pk
        )

    def Boolean(required:bool=False,
            default:bool=None,
            help_text:str=None,
            unique=True):

        return Column(
            BooleanType,
            nullable=True if not required else False,
            unique=unique,
            default=default
        )
    
    def Json(self, required:bool=False,
            default:dict=dict(),
            help_text:str=None) -> Column:
        
        return Column(
            JSONType(enforce_string=True, enforce_unicode=False), 
            nullable= True if not required else False,
            default=default
            )

    def Image(self, required:bool=True,
            help_text:str = None
            ) -> Column:

        return Column(
                ImageType(255),
                nullable= True if not required else False
        )

    def Binary(required:bool=False,
            default:bytes=None,
            help_text:str=None,
            unique=True):

        return Column(
            LargeBinaryType,
            nullable=True if not required else False,
            unique=unique,
            default=default
        )

    def LargeBinary(required:bool=False,
            default:bytes=None,
            help_text:str=None,
            unique=True):

        return Column(
            LargeBinaryType,
            nullable=True if not required else False,
            unique=unique,
            default=default
        )