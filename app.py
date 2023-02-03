from flask import Flask

import auth
import views
import settings


app = Flask(__name__)
app.secret_key = settings.secret_key
app.config.from_object(settings.configClass)

auth.login_manager.init_app(app)

app.register_blueprint(views.main_bp)
app.register_blueprint(auth.auth_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
