import os
import re
from typing import Any
from urllib.parse import urlparse, urlunparse, parse_qs

from storages.backends.s3 import S3Storage

from . import ExtendedStorage


class S3ExtendedStorage(ExtendedStorage, S3Storage): # type: ignore
    @classmethod
    def get_storage_kwargs_from_path(cls, location: Any) -> dict[str,Any]:
        if not isinstance(location, str):
            raise TypeError(f"path: {type(location).__name__}")
        
        if location.startswith('s3:'):
            url = location[3:]
        else:
            url = location
        
        url_r = urlparse(url)
        endpoint = urlunparse((url_r.scheme, url_r.netloc, '', '', '', ''))
        
        url_query = parse_qs(url_r.query)
        region = url_query.pop('region')[-1] if url_query.get('region') else None
        bucket = url_query.pop('bucket')[-1] if url_query.get('bucket') else None
        prefix = url_query.pop('prefix')[-1] if url_query.get('prefix') else None
        
        if m := re.match(r'^/(?P<bucket>[^/]+)(?:/(?P<prefix>.*))?$', url_r.path):
            bucket = m['bucket']
            if m['prefix'] is not None:
                prefix = m['prefix']

        # See https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#authentication-settings
        access_key = None  # environment variable AWS_S3_ACCESS_KEY_ID or AWS_ACCESS_KEY_ID 
        secret_key = None  # environment variable AWS_S3_SECRET_ACCESS_KEY or AWS_SECRET_ACCESS_KEY 
        
        # (Scaleway specific)
        if m := re.match(r'^s3\.(?P<region>[a-z0-9\-]+)\.scw\.cloud$', url_r.netloc):
            region = m['region']            
            access_key = os.environ.get('SCW_ACCESS_KEY')
            secret_key = os.environ.get('SCW_SECRET_KEY')
                
        kwargs: dict[str,Any] = {
            'endpoint_url': endpoint,
        }

        if region:
            kwargs['region_name'] = region
        if bucket:
            kwargs['bucket_name'] = bucket
        if prefix:
            kwargs['location'] = prefix
        if access_key:
            kwargs['access_key'] = access_key
        if secret_key:
            kwargs['secret_key'] = secret_key

        proxies = {}
        if proxy := os.environ.get('HTTPS_PROXY'):
            proxies['https'] = proxy
        if proxy := os.environ.get('HTTP_PROXY'):
            proxies['http'] = proxy
        if proxies:
            kwargs['proxies'] = proxies

        return kwargs

    
    @property
    def is_versioning_enabled(self):
        status: str = self.connection.BucketVersioning(self.bucket_name).status # type: ignore - Value is empty, "Enabled", or "Suspended"
        return status == "Enabled"

