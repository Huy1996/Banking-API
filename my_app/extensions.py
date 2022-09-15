from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_uuid import FlaskUUID
from flask_s3 import FlaskS3


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
flask_uuid = FlaskUUID()
flask_s3 = FlaskS3()


