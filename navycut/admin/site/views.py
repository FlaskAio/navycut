import typing
from json import dumps
from warnings import warn
from flask_admin import AdminIndexView
from navycut.auth import current_user
from flask import redirect, render_template_string as rts, url_for
from flask_admin._compat import string_types, urljoin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField, ImageUploadInput
from flask_admin.contrib.sqla.form import AdminModelConverter
from navycut.conf import get_settings_module
from wtforms.widgets import html_params, TextArea
from wtforms import fields, validators, TextAreaField
from dotenv import load_dotenv; load_dotenv()
from navycut.orm.sqla.types import ImageType
from sqlalchemy import Boolean, Column
from sqlalchemy.types import Text as TextType
from sqlalchemy.orm import ColumnProperty
from flask_admin import form
from flask_admin.model.form import  FieldPlaceholder
from flask_admin.contrib.sqla.validators import Unique
from flask_admin.contrib.sqla.tools import (has_multiple_pks, 
                                    filter_foreign_columns,
                                    is_association_proxy)

from flask_admin.form.fields import JSONField as _JsonField
from sqlalchemy_jsonfield import JSONField as JSONType

class JSONField(_JsonField):
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data:
            return dumps(self.data, ensure_ascii=False, indent=2)
        else:
            return ''

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class _ImageUploadInput(ImageUploadInput):
    
    input_type = 'file'
    
    pre_image_html = (
        """
        <input onchange="readImage{{context.name | safe}}(this)" {{context.file | safe}}>
        <div class="image-thumbnail">
            <img id="{{context.name | safe}}_image" src="https://via.placeholder.com/120" style="margin : 10px;">
        </div>
        <script>
            function readImage{{context.name | safe}}(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#{{context.name | safe}}_image')
                            .attr('src', e.target.result)
                    };

                    reader.readAsDataURL(input.files[0]);
                }
            }
        </script>
        """
        )

    post_image_html = (
        """
        <div class="image-thumbnail">
            <img id="{{context.name | safe}}_image" {{context.image | safe}}>
            <input type="checkbox" name="{{context.marker | safe}}">Delete</input>
            <input{{context.text | safe}}>
        </div>
        <input onchange="readImage{{context.name | safe}}(this)" {{context.file | safe}}>
        <script>
            function readImage{{context.name | safe}}(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#{{context.name | safe}}_image')
                            .attr('src', e.target.result)
                            .css("margin-bottom", "10px");
                    };
                    reader.readAsDataURL(input.files[0]);
                }
            }
        </script>
        """
    )

    def __init__(self, *wargs, **kwargs) -> None:
        super(_ImageUploadInput, self).__init__(*wargs, **kwargs)

    def __call__(self, field, **kwargs) -> str:
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        context = dict(
            name = field.name,
            file = html_params(type='file', **kwargs),
            marker = f'_{field.name}-delete',
            text = html_params(type='hidden', value=field.data, name=field.name)
            )
        if field.data and isinstance(field.data, string_types):
            url = self.get_url(field)
            context.update(dict(image=html_params(src=url)))
            template = self.post_image_html
        else: 
            template = self.pre_image_html
        return rts(template, context=context)

    def get_url(self, field):

        # overriding the default get_url method.

        if field.thumbnail_size:
            filename = field.thumbnail_fn(field.data)
        else:
            filename = field.data

        return urljoin(field.url_relative_path, filename)

class _ImageUploadField(ImageUploadField):

    widget= _ImageUploadInput()

    def __init__(self, *wargs, **kwargs):
        settings = get_settings_module()
        super(_ImageUploadField, self).__init__(*wargs, **kwargs)
        self.base_path = str(settings.BASE_DIR / "uploads/images/")
        self.url_relative_path = "/static_upload/images/"


class NavAdminIndexView(AdminIndexView):

    def __init__(self, *args, **kwargs):
        super(NavAdminIndexView, self).__init__(*args, **kwargs)
        self.endpoint = "admin_index"
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')


class _AdminModelConverter(AdminModelConverter):
    
    def __init__(self, session, view) ->typing.NoReturn:
        super(_AdminModelConverter, self).__init__(session, view)

    def _get_description(self, name, field_args):
        """
        overriding the default _get_description method
        to return the help text for a field from model.
        """
        for column in self.view.model.__table__.columns:
            if hasattr(column, 'help_text') and not name != column.name:
                return column.help_text

    def _get_field_override(self, name:typing.AnyStr) -> typing.Any:
        """
        overriding the default _get_field_override method
        to return NC's own ImageUploadField class.
        """
        for column in self.view.model.__table__.columns:
            if isinstance(column.type, ImageType) and not name != column.name: 
                #return the image field if the column 
                # type is matched with the ImageType.

                return _ImageUploadField
            
            if isinstance(column.type, TextType) and not name != column.name:
                return CKTextAreaField

            if isinstance(column.type, JSONType) and not name != column.name:
                return JSONField

    def convert(self, model, mapper, name, prop, field_args, hidden_pk):
        """
        overriding the default convert method to
        change the choices system.
        """
        # Properly handle forced fields
        if isinstance(prop, FieldPlaceholder):
            return form.recreate_field(prop.field)

        kwargs = {
            'validators': [],
            'filters': []
        }

        if field_args:
            kwargs.update(field_args)

        if kwargs['validators']:
            # Create a copy of the list since we will be modifying it.
            kwargs['validators'] = list(kwargs['validators'])

        # Check if it is relation or property
        if hasattr(prop, 'direction') or is_association_proxy(prop):
            property_is_association_proxy = is_association_proxy(prop)
            if property_is_association_proxy:
                if not hasattr(prop.remote_attr, 'prop'):
                    raise Exception('Association proxy referencing another association proxy is not supported.')
                prop = prop.remote_attr.prop
            return self._convert_relation(name, prop, property_is_association_proxy, kwargs)
        elif hasattr(prop, 'columns'):  # Ignore pk/fk
            # Check if more than one column mapped to the property
            if len(prop.columns) > 1 and not isinstance(prop, ColumnProperty):
                columns = filter_foreign_columns(model.__table__, prop.columns)

                if len(columns) == 0:
                    return None
                elif len(columns) > 1:
                    warn('Can not convert multiple-column properties (%s.%s)' % (model, prop.key))
                    return None

                column = columns[0]
            else:
                # Grab column
                column = prop.columns[0]

            form_columns = getattr(self.view, 'form_columns', None) or ()

            # Do not display foreign keys - use relations, except when explicitly instructed
            if column.foreign_keys and prop.key not in form_columns:
                return None

            # Only display "real" columns
            if not isinstance(column, Column):
                return None

            unique = False

            if column.primary_key:
                if hidden_pk:
                    # If requested to add hidden field, show it
                    return fields.HiddenField()
                else:
                    # By default, don't show primary keys either
                    # If PK is not explicitly allowed, ignore it
                    if prop.key not in form_columns:
                        return None

                    # Current Unique Validator does not work with multicolumns-pks
                    if not has_multiple_pks(model):
                        kwargs['validators'].append(Unique(self.session,
                                                           model,
                                                           column))
                        unique = True

            # If field is unique, validate it
            if column.unique and not unique:
                kwargs['validators'].append(Unique(self.session,
                                                   model,
                                                   column))

            optional_types = getattr(self.view, 'form_optional_types', (Boolean,))

            if (
                not column.nullable and
                not isinstance(column.type, optional_types) and
                not column.default and
                not column.server_default
            ):
                kwargs['validators'].append(validators.InputRequired())

            # Apply label and description if it isn't inline form field
            if self.view.model == mapper.class_:
                kwargs['label'] = self._get_label(prop.key, kwargs)
                kwargs['description'] = self._get_description(prop.key, kwargs)

            # Figure out default value
            default = getattr(column, 'default', None)
            value = None

            if default is not None:
                value = getattr(default, 'arg', None)

                if value is not None:
                    if getattr(default, 'is_callable', False):
                        value = lambda: default.arg(None)  # noqa: E731
                    else:
                        if not getattr(default, 'is_scalar', True):
                            value = None

            if value is not None:
                kwargs['default'] = value

            # Check nullable
            if column.nullable:
                kwargs['validators'].append(validators.Optional())

            # Override field type if necessary
            override = self._get_field_override(prop.key)
            if override:
                return override(**kwargs)

            # Check if a list of 'form_choices' are specified

            # adding the default choice system from here. 

            if mapper.class_ == self.view.model and hasattr(column, "choices"):
                choices = getattr(column, "choices")
                if choices:
                    return form.Select2Field(
                        choices=choices,
                        allow_blank=column.nullable,
                        **kwargs
                    )

            # Run converter
            converter = self.get_converter(column)

            if converter is None:
                return None

            return converter(model=model, mapper=mapper, prop=prop,
                             column=column, field_args=kwargs)
        return None

class NCAdminModelView(ModelView):
    
    model_form_converter = _AdminModelConverter

    can_export = True

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    def __init__(self, *wargs, **kwargs):
        super(NCAdminModelView, self).__init__(*wargs, **kwargs)