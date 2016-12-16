# Local Files
from handlers import site
from flask_login import LoginManager
from user import User, UserDatabaseOPS

# Modules
from flask import Flask, render_template
import os

app = Flask(__name__)

lm = LoginManager()

def create_app():
    app.config.from_object('settings')
    app.register_blueprint(site)
    lm.init_app(app)
    lm.login_view = 'site.login_page'
    app.secret_key = '8Z~sr0X6I8pgBge'
    return app


@lm.user_loader
def load_user(user_id):
    return UserDatabaseOPS.select_user_with_id(user_id)

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':

    app = create_app()

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.run(host='0.0.0.0', port=port, debug=debug)
