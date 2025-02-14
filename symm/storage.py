from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class MaterialAttachmentStorage(S3Boto3Storage):
    location = 'material_attachments'
    file_overwrite = False

    def get_default_settings(self):
        defaults = super().get_default_settings()
        defaults.update({
            'bucket_name': settings.AWS_STORAGE_BUCKET_NAME,
            'access_key': settings.AWS_ACCESS_KEY_ID,
            'secret_key': settings.AWS_SECRET_ACCESS_KEY,
            'endpoint_url': getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
#            'use_ssl': settings.AWS_S3_USE_SSL,
        })
        return defaults
