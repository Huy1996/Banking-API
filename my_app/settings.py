import os
from dotenv import find_dotenv, load_dotenv
from my_app.utils import CustomJSONEncoder
from datetime import timedelta

load_dotenv(find_dotenv())

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PROPAGATE_EXCEPTIONS = True

RESTFUL_JSON = {'cls': CustomJSONEncoder}
BUNDLE_ERRORS = True

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_REGION = os.environ.get('S3_REGION')