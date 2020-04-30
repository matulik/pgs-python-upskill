import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import sys

class AWS:
    def __init__(self):
        self._s3 = boto3.resource('s3')
        self._bucket = self._s3.Bucket('kmatula-upskill')

    def upload(self, key, data):
        self._bucket.put_object(Key=key, Body=data)

    def create_presigned_url(self, object_name, expiration=7200):
        client = boto3.client('s3', config=Config(signature_version='s3v4'))
        try:
            response = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self._bucket.name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
        except ClientError as e:
            print('AWS error: {}'.format(e.__str__()), file=sys.stdout)
            return None
        return response


