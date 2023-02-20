from flask import Flask
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
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = settings.secret_key
app.config.from_object(settings.configClass)

db.init_app(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Insurance', template_mode='bootstrap4')


class PolicyView(ModelView):
    column_hide_backrefs = False
    # column_list = ("strike_event")
    # inline_models = (Event,)
    column_list = ('name',
                   'description',
                   'start_date',
                   'end_date',
                   'premium',
                   'coverage_amount',
                   'strike_event'
                   )

    # def __init__(self, session, **kwargs):
    #     super(PolicyView, self).__init__(Policy, session, **kwargs)


class EventView(ModelView):
    column_hide_backrefs = False
    # column_list = ("policy_id")
    # inline_models = (Policy,)
    # def __init__(self, session, **kwargs):
    #     super(StrikeEventView, self).__init__(StrikeEvent, session, **kwargs)


class UserView(ModelView):
    column_hide_backrefs = False
    column_list = ("wallet_address",)


class FarmView(ModelView):
    column_hide_backrefs = False


admin.add_view(PolicyView(model=Policy, session=db.session))
admin.add_view(EventView(model=Event, session=db.session))
admin.add_view(UserView(model=User, session=db.session))
admin.add_view(ModelView(model=Role, session=db.session))
admin.add_view(FarmView(model=Farm, session=db.session))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Weather=Weather)


auth.login_manager.init_app(app)

app.register_blueprint(views.main_bp)
app.register_blueprint(auth.auth_bp)
app.register_blueprint(data.data_bp)

# def seed_db():
#     # with app.app_context():
#     user_role = Role(name='farmer')
#     super_user_role = Role(name='admin')
#     db.session.add(user_role)
#     db.session.add(super_user_role)
#     db.session.commit()


if __name__ == "__main__":
    # db.create_all()
    # with app.app_context():
    # seed_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
