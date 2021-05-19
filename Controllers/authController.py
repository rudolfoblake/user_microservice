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

    def password_decode(self, password: bytes) -> str:
        try:
            return base64.b64decode(password.encode("utf8")).decode("utf8")
        except:
            return ""

    def encrypt(self, content: bytes, key: str) -> bytes:
        key = bytes(key.encode())
        f = Fernet(key)
        token = f.encrypt(bytes(content.encode()))
        return token
        
    def is_encrypted(self, content: str) -> bool:
        if type(content) == bytes:
            return True
        return False

    def decrypt(self, content: str, key: bytes) -> str:
        f = Fernet(key)
        return str(f.decrypt(content).decode())
