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
    # Bind to PORT/HOST if defined, otherwise default to 5050/localhost.
    app = create_app()
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    app.run(host=HOST, port=PORT)