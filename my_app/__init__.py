from flask import Flask
from my_app.extensions import db, bcrypt, jwt, flask_uuid
from my_app.blueprints import users


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    app.app_context().push()

    #--------Initialize Extension---------#
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    flask_uuid.init_app(app)


    #--------Register Blueprint___________#
    app.register_blueprint(users)

    db.create_all()
    @app.before_first_request
    def create_db():
        db.create_all()

    return app
