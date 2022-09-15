from flask import Flask
from .extensions import db, bcrypt, jwt, flask_uuid, flask_s3
from .blueprints import users, accounts, upload


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    app.app_context().push()

    #--------Initialize Extension---------#
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    flask_uuid.init_app(app)
    flask_s3.init_app(app)


    #--------Register Blueprint___________#
    app.register_blueprint(users)
    app.register_blueprint(accounts)
    app.register_blueprint(upload)


    db.create_all()
    @app.before_first_request
    def create_db():
        db.create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app

