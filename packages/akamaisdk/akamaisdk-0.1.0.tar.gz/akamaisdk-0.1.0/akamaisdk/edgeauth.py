import hashlib
import hmac
import base64
import time
import uuid
from urllib.parse import urlparse

class EdgeAuth:
    def __init__(self, client_token, client_secret, access_token, base_url):
        self.client_token = client_token
        self.client_secret = client_secret.encode()
        self.access_token = access_token
        self.base_url = base_url.rstrip("/")

    def auth_headers(self, method, path, body=''):
        timestamp = time.strftime('%Y%m%dT%H:%M:%S+0000', time.gmtime())
        nonce = str(uuid.uuid4())

        parsed_url = urlparse(self.base_url + path)
        canonical_request = self._canonicalize_request(method, parsed_url, body)

        signing_key = hmac.new(self.client_secret, timestamp.encode('utf-8'), hashlib.sha256).digest()
        auth_data = (
            f'client_token={self.client_token};'
            f'access_token={self.access_token};'
            f'timestamp={timestamp};'
            f'nonce={nonce}'
        )

        signing_data = f'{auth_data}\n{canonical_request}'
        signature = base64.b64encode(hmac.new(signing_key, signing_data.encode('utf-8'), hashlib.sha256).digest()).decode()

        auth_header = f'EG1-HMAC-SHA256 {auth_data};signature={signature}'
        return {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }

    def _canonicalize_request(self, method, parsed_url, body):
        path = parsed_url.path or '/'
        query = parsed_url.query
        host = parsed_url.hostname.lower()

        content_hash = hashlib.sha256(body.encode('utf-8') if body else b'').hexdigest()

        return f'{method.upper()}\thttps\t{host}\t{path}\t{query}\t{content_hash}'