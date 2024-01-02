from app import app, db

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form import SecureForm, ImageUploadField
from flask_admin.contrib.sqla import ModelView
import PIL

from wtforms.meta import DefaultMeta
from flask_wtf.csrf import _FlaskFormCSRF

from flask import redirect, current_app, session, Blueprint
from flask_login import current_user

import os

admin = Blueprint('shopadmin', __name__)

app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

class DashboardView(AdminIndexView):
    def is_visible(self):
        return False

usr_admin = Admin(app, name='Shop Admin', template_mode='bootstrap4', index_view=DashboardView())

upload_path = os.path.join(os.path.dirname(__file__), 'look/')

try:
    os.mkdir(upload_path)
except OSError:
    pass

from modules.models import Cord

class CustomSecureForm(SecureForm):
    class Meta(DefaultMeta):
        csrf_class = _FlaskFormCSRF
        csrf_context = session

        @property
        def csrf_secret(self):
            return current_app.config.get('WTF_CSRF_SECRET_KEY',
                                          current_app.secret_key)

class CordAdmin(ModelView):
    form_base_class = CustomSecureForm
    form_columns = ['id', 'name', 'price', 'desc', 'image']
    page_size = 15
    column_searchable_list = ['name', 'price']
    column_filters = ['name', 'price']
    column_editable_list = ['name', 'name', 'price', 'desc', 'image']
    can_view_details = True

    form_extra_fields = {
        'image': ImageUploadField(
            'image',
            base_path=upload_path
        )
    }

    def on_model_delete(self, model):
        if model.image:
            try:
                image_path = os.path.join(upload_path, model.image)
                os.remove(image_path)
            except:
                pass

    def is_accessible(self):
        return True if current_user.is_superuser else False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')
#Adding views to display in admin panel
usr_admin.add_view(CordAdmin(Cord, db.session))


# @admin.route('/admin')
# def administrator():
#     '''Only seen by administrator accounts'''
    
#     if current_user.is_superuser:
#         return ('You are admin!')
#     else:
#         return ('Please validate yourself!')
#     #return ('administrator')