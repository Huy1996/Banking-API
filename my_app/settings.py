import os
from dotenv import find_dotenv, load_dotenv
from my_app.middleware import CustomJSONEncoder

load_dotenv(find_dotenv())

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
PROPAGATE_EXCEPTIONS = True
RESTFUL_JSON = {'cls': CustomJSONEncoder}
