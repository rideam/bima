from flask import Flask, Response
from flask_migrate import Migrate

import views
import settings
from routes import *

from models import db, \
    Weather, \
    Policy, \
    Event, \
    Farm, \
    Role, \
    User
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config.from_object(settings.configClass)
auth = HTTPBasicAuth()

users = {
    settings.admin_user: generate_password_hash(settings.admin_pwd)
}

db.init_app(app)
migrate = Migrate(app, db)


@auth.verify_password
def verify_password(username, password):
    """ Verify admin username and password for the admin page
    """

    if username in users and \
            check_password_hash(users.get(username), password):
        return username


login_required_view = auth.login_required(lambda: None)


def is_authenticated():
    try:
        return login_required_view() is None
    except HTTPException:
        return False


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}))


# class MyModelView(ModelView):
#     def is_accessible(self):
#         if not is_authenticated():
#             raise AuthException('Not authenticated.')
#         else:
#             return True


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):

        if not is_authenticated():
            raise AuthException('Not authenticated.')
        else:
            return True


class PolicyView(ModelView):
    column_hide_backrefs = False
    # inline_models = (Event,)
    column_list = ('name',
                   'description',
                   'start_date',
                   'end_date',
                   'premium',
                   'coverage_amount',
                   'strike_event'
                   )


class EventView(ModelView):
    column_hide_backrefs = False


class UserView(ModelView):
    column_hide_backrefs = False
    column_list = ("wallet_address",)


class FarmView(ModelView):
    column_hide_backrefs = False


class RoleView(ModelView):
    column_hide_backrefs = True


admin = Admin(app, name='Bima', template_mode=settings.template_mode, index_view=MyAdminIndexView())
admin.add_view(UserView(model=User, session=db.session))
admin.add_view(RoleView(model=Role, session=db.session))
admin.add_view(FarmView(model=Farm, session=db.session))
admin.add_view(PolicyView(model=Policy, session=db.session))
admin.add_view(EventView(model=Event, session=db.session))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Weather=Weather)


appauth.login_manager.init_app(app)

app.register_blueprint(views.main_bp)
app.register_blueprint(appauth.auth_bp)
app.register_blueprint(data.data_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
