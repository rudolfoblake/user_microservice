import base64
from cryptography.fernet import Fernet

class AuthControl:
    def password_encode(self, password: str) -> str:
        try:
            return base64.b64encode(password.encode("utf8")).decode("utf8")
        except:
            return ""

    def password_is_encoded(self, password: str) -> bool:
        try:
            base64.b64decode(password.encode("utf8")).decode("utf8")
        except:
            return False
        return True

    def password_decode(self, password: str) -> str:
        try:
            return base64.b64decode(password.encode("utf8")).decode("utf8")
        except:
            return ""
