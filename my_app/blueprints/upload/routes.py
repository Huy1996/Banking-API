from flask import Blueprint
from flask_restful import Api
from .resources import Upload

upload = Blueprint('upload', __name__, url_prefix='/upload')

api = Api(upload)
api.add_resource(Upload, '/')