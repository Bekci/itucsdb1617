# Local Files
from handlers import site

# Modules
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site)
    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()