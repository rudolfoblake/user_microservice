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

    def encrypt(self, content: str, key: str) -> str:
        key = bytes(key.encode())
        f = Fernet(key)
        token = f.encrypt(bytes(content.encode()))
        return str(token.decode())
        
    def is_encrypted(self, content: str, key: str) -> bool:
        try:
            self.decrypt(content, key)
        except:
            return False
        return True

    def decrypt(self, content: str, key: str) -> str:
        f = Fernet(bytes(key.encode()))
        return str(f.decrypt(bytes(content.encode())).decode())
