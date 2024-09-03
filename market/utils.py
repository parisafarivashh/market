import base64

import pyotp
from .settings import SECRET_KEY


def generate_totp(phone: str) -> str:
    base32_secret = _get_secrete_key(phone)
    totp = pyotp.TOTP(base32_secret, digits=4)
    return totp.now()

def validate_totp(phone: str, code: str) -> bool:
    base32_secret = _get_secrete_key(phone)
    totp = pyotp.TOTP(base32_secret)
    is_valid = totp.verify(code)
    return is_valid

def _get_secrete_key(phone: str) -> str:
    unique_key = f"{phone}{SECRET_KEY[::11]}"  # unique
    base32_secret = base64.b32encode(unique_key.encode('utf-8')).decode('utf-8')
    return base32_secret

