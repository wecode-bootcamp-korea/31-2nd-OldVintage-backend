import boto3, uuid

from oldvintage.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

class FileUploader:
    def __init__(self, client, bucket_name):
        self.client      = client
        self.bucket_name = bucket_name
        
    def upload(self, file):
        try: 
            file_id    = 'static/review/' + str(uuid.uuid4().hex) + '_' + file.name
            extra_args = {'ContentType' : file.content_type}

            self.client.upload_fileobj(
                file,
                self.bucket_name,
                file_id,
                ExtraArgs = extra_args
            )
            return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
        except:
            return None

    def delete(self, file_name):
        return self.client.delete_object(bucket=self.config.bucket_name, Key=f'{file_name}')

class FileHandler:
    def __init__(self, client):
        self.client = client
    
    def upload(self, file):
        return self.client.upload(file)

    def delete(self, file_name):
        return self.client.delete(file_name)

file_uploader = FileUploader(
                    boto3.client(
                        's3',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY),
                        AWS_STORAGE_BUCKET_NAME)

file_handler  = FileHandler(file_uploader)