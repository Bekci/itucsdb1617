# Local Files
from handlers import site
import os

# Modules
from flask import Flask

app = Flask(__name__)

def create_app():

    app.config.from_object('settings')
    app.register_blueprint(site)
    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.run(host='0.0.0.0', port=port, debug=debug)