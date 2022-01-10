import boto3, os
from flask import current_app as app, g

s3_resource = boto3.resource('s3')
client = boto3.client('s3')

##########################################################################################################################################

class S3Handler():
    """A class dedicated to communicating with AWS S3's server"""
    
    @classmethod
    def create_user_image_storage_in_s3(self, user_id):
        """Creates the object in AWS S3 storage upon user signup"""
        
        body = f'users/{user_id}/profile.png'
        key = f'users/{user_id}/profile.png'
        bucket = 'gamehunter'
        content_type = 'image/jpeg'
        client.put_object(Body=body,Bucket=bucket,Key=key,ContentType=content_type)


    @classmethod
    def upload_user_image(self, user_id):
        """Uploads the User submitted image to AWS S3 storage."""
        
        file = f'blueprints/users/tempFolder/{g.user.id}profile.png'
        bucket = 'gamehunter'
        key = f'users/{user_id}/profile.png'
        
        s3_resource.meta.client.upload_file(file, bucket, key)
    
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}profile.png'))