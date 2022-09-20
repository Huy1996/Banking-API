from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from my_app.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, S3_REGION
from time import time_ns
import boto3


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=S3_REGION
)


class Upload(Resource):
    @jwt_required()
    def post(self):
        file = request.files['file']
        file_name = f'{time_ns()}.jpg'
        s3.upload_fileobj(file, S3_BUCKET_NAME, file_name, ExtraArgs={'ACL': 'public-read'})

        file_url = '%s/%s/%s' % (s3.meta.endpoint_url, S3_BUCKET_NAME, file_name)
        return {'image': file_url}, 200