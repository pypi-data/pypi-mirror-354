import base64
import logging
from pathlib import Path

import httpx
import machineid
from cryptography.hazmat.primitives import serialization, hashes

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Vault(object):

    def __init__(self, base_url: str, app_name: str, pub_key: str, features: list = None, license: str = None):
        self._base_url = base_url
        self._machine_id = machineid.id()
        self._app_name = app_name
        self._pub_key = None
        if isinstance(pub_key, str) and Path(pub_key).exists():
            self._pub_key = open(pub_key, 'rb').read()
        elif isinstance(pub_key, bytes):
            self._pub_key = pub_key
        else:
            raise TypeError('Invalid public key')
        self._features = features
        self._license = license
        self._logger = logging.getLogger(self._app_name)
        pass

    @property
    def machine_id(self):
        return self.machine_id

    @property
    def app_name(self):
        return self._app_name

    @property
    def valid(self) -> bool:
        pass

    def activate(self):
        try:
            resp = httpx.post(self._base_url, json=data, timeout=5)
            resp.raise_for_status()

        except httpx.RequestError as ex:
            self._logger.error(f"RequestError: {ex.request.url} -> {ex}")
        except httpx.HTTPStatusError as ex:
            print(f"HTTPStatusError {ex.response.status_code}：{ex.response.text}")
        return None

    def verify(self, license: str):

        def _aes_decrypt_(ciphertext):
            from cryptography.hazmat.primitives import padding

            aes_key = base64.b64encode(str(self.machine_id).encode())[:256]
            aes_iv = base64.b64encode(str(self.app_name).encode())[:16]
            aes_cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv))
            aes_decryptor = aes_cipher.decryptor()
            padded_data = aes_decryptor.update(signature) + aes_decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            return unpadder.update(padded_data) + unpadder.finalize()

        def _rsa_verify_(message, signature):
            from cryptography.hazmat.primitives.asymmetric import padding

            if not isinstance(self._pub_key, bytes):
                raise TypeError('PUBLIC_KEY_INVALID')
            try:
                public_key = serialization.load_pem_public_key(self._pub_key)
                public_key.verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
            except Exception:
                raise ValueError('LICENSE_INVALID')

        try:
            signature = base64.b64decode(license)
            license_data = _aes_decrypt_(signature).split(b'|')

        except Exception as e:
            self._logger.error(f"Invalid license: {e}")
            return False
