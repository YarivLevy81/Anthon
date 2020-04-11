from flask import Flask


def create_app():

    app = Flask(__name__, template_folder='template')

    from .routes import main
    app.register_blueprint(main)

    localhost = "127.0.0.1"
    app.config['host'] = localhost
    app.config['port'] = 8080
    app.config['api_host'] = localhost
    app.config['api_port'] = 5000

    return app
