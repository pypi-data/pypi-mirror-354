import re
from datetime import timedelta

from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin
from google.oauth2 import service_account
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class StorageMixin:
    object_parameters = {
        "cache_control": f"max-age={60 * 60 * 24 * 7}, s-maxage={60 * 60 * 24 * 7}, must-revalidate"
    }
    default_acl = "publicRead"
    file_overwrite = False
    retry = True


class ManifestStaticFilesStorage(StorageMixin, ManifestFilesMixin, GoogleCloudStorage):
    bucket_name = setting("STATIC_BUCKET_NAME")
    custom_endpoint = setting("STATIC_CUSTOM_ENDPOINT")
    location = setting("STATIC_LOCATION", "")
    manifest_name = setting("STATIC_MANIFEST_NAME", ManifestFilesMixin.manifest_name)
    credentials = (
        service_account.Credentials.from_service_account_info(
            setting("STATIC_CREDENTIALS")
        )
        if setting("STATIC_CREDENTIALS")
        else None
    )
    vite_hash_pattern = r"^.+[\.-][0-9a-zA-Z_-]{8,12}\..+$"

    def url(self, name, force=False):
        # if the file already has a hash, we don't need the django hashed file
        if re.match(self.vite_hash_pattern, name):
            return super(HashedFilesMixin, self).url(name)
        return super().url(name, force)


class MediaStorage(StorageMixin, GoogleCloudStorage):
    bucket_name = setting("MEDIA_BUCKET_NAME")
    location = setting("MEDIA_LOCATION", "")
    custom_endpoint = setting("MEDIA_CUSTOM_ENDPOINT")
    credentials = (
        service_account.Credentials.from_service_account_info(
            setting("MEDIA_CREDENTIALS")
        )
        if setting("MEDIA_CREDENTIALS")
        else None
    )


class PrivateFilesStorage(StorageMixin, GoogleCloudStorage):
    bucket_name = setting("MEDIA_BUCKET_NAME")
    location = setting("PRIVATE_LOCATION", "private/")
    custom_endpoint = None
    default_acl = "private"
    file_overwrite = False
    expiration = timedelta(hours=1)
    credentials = (
        service_account.Credentials.from_service_account_info(
            setting("MEDIA_CREDENTIALS")
        )
        if setting("MEDIA_CREDENTIALS")
        else None
    )


class ThumbnailStorage(MediaStorage):
    file_overwrite = True
