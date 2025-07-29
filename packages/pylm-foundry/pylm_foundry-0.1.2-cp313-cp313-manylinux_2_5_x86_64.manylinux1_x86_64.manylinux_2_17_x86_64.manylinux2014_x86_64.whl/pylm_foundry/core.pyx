import base64
import json
from datetime import datetime, timedelta
from pathlib import Path

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher


class Foundry(object):
    def __init__(self, app_name: str, license_key: str | bytes = None, encrypt_key: str | bytes = None):
        self._app_name = app_name
        self._license_key = None
        self._encrypt_key = None
        if isinstance(license_key, str) and Path(license_key).exists():
            self._license_key = open(license_key, 'rb').read()
        elif isinstance(license_key, bytes):
            self._license_key = license_key
        if isinstance(encrypt_key, str) and Path(encrypt_key).exists():
            self._encrypt_key = open(encrypt_key, 'rb').read()
        elif isinstance(encrypt_key, bytes):
            self._encrypt_key = encrypt_key
        if not isinstance(self._license_key, bytes):
            key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self._license_key = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )

    @property
    def license_key(self) -> bytes:
        return self._license_key

    @property
    def encrypt_key(self) -> bytes:
        return self._encrypt_key

    def generate(self, machine_id: str, features: list = None, expire_secs: int = 86400):

        def _aes_encrypt_(machine_id, app_name, plaintext):
            from cryptography.hazmat.primitives import padding

            aes_key = base64.b64encode(str(machine_id).encode())[:256]
            aes_iv = base64.b64encode(str(app_name).encode())[:16]
            aes_cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv))
            aes_encryptor = aes_cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            ciphertext = aes_encryptor.update(padded_data) + aes_encryptor.finalize()
            return ciphertext

        def _rsa_sign_(message, signature):
            from cryptography.hazmat.primitives.asymmetric import padding

            if not isinstance(self._license_key, bytes):
                raise TypeError('LICENSE_KEY_INVALID')
            private_key = serialization.load_pem_private_key(self._license_key, password=None)
            signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
            return signature

        license_data = {
            'machine_id': machine_id,
            'app_name': self._app_name,
            'features': features or [],
            'expire_date': datetime.now() + timedelta(seconds=expire_secs),
        }
        message = json.dumps(license_data, sort_keys=True).encode()
        private_key = serialization.load_pem_private_key(self._license_key, password=None)
        signature = private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())
        return base64.b64encode(signature).decode()
