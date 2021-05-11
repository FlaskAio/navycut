from flask_admin import AdminIndexView
from .auth import current_user
from flask import redirect, render_template_string as rts
from flask_admin._compat import string_types
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField, ImageUploadInput
from flask_admin.contrib.sqla.form import AdminModelConverter
from navycut.conf import get_settings_module
from wtforms.widgets import html_params
from dotenv import load_dotenv; load_dotenv()

class _ImageUploadInput(ImageUploadInput):
    
    input_type = 'file'
    
    pre_image_html = (
        """
        <input onchange="readImage(this)" {{context.file | safe}}>
        <img id="demo_image" src="https://via.placeholder.com/120" style="margin : 10px; max-height:100px; max-width: 100px;">
        <script>
            function readImage(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#demo_image')
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
            <img id="demo_image" {{context.image | safe}}>
            <input type="checkbox" name="{{context.marker | safe}}">Delete</input>
            <input{{context.text | safe}}>
        </div>
        <input onchange="readImage(this)" {{context.file | safe}}>
        <script>
            function readImage(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#demo_image')
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

class _ImageUploadField(ImageUploadField):

    widget= _ImageUploadInput()

    def __init__(self, *wargs, **kwargs):
        settings = get_settings_module()
        super(_ImageUploadField, self).__init__(*wargs, **kwargs)
        self.base_path = str(settings.BASE_DIR / "uploads/images/")
        self.url_relative_path = "images/"
        self.endpoint = "navycut.helpers.static_server.static"


class NavAdminIndexView(AdminIndexView):
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/admin/login')


class _AdminModelConverter(AdminModelConverter):
    
    def __init__(self, session, view):
        super(_AdminModelConverter, self).__init__(session, view)

    def _get_field_override(self, name):
        if name.endswith("_image") or name.endswith("_picture"):
            return _ImageUploadField


class NCSpecialModelView(ModelView):
    
    model_form_converter = _AdminModelConverter
    
    def __init__(self, *wargs, **kwargs):
        super(NCSpecialModelView, self).__init__(*wargs, **kwargs)