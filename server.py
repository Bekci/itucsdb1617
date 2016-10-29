# Local Files
from handlers import site

# Modules
from flask import Flask
import os

app = Flask(__name__)


def create_app():
    app.config.from_object('settings')
    app.register_blueprint(site)
    return app

if __name__ == '__main__':

    app = create_app()

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.run(host='0.0.0.0', port=port, debug=debug)