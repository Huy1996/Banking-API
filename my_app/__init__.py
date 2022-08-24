from flask import Flask
from my_app.extensions import db, bcrypt, jwt, uuid
from my_app.users import users


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)


    #--------Initialize Extension---------#
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    uuid.init_app(app)


    #--------Register Blueprint___________#
    app.register_blueprint(users)


    @app.before_first_request
    def create_db():
        db.create_all()

    return app

