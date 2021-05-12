import base64
from cryptography.fernet import Fernet

class AuthControl:
    def password_encode(self, password: str) -> str:
        try:
            return base64.b64encode(password.encode("UTF-8")).decode("UTF-8")
        except:
            return ""

    def password_is_encoded(self, password: str) -> bool:
        if "=" in password:
            return True
        return False

    def password_decode(self, password: str) -> str:
        try:
            return base64.b64decode(password)
        except:
            return password

    def password_encrypt(self, password: str, key: str) -> str:
        try:
            f = Fernet(Fernet.generate_key())
            password = f.encrypt(self.password_decode(password))
        except:
            return ""
        return password

    def password_decrypt(self, password: str, key: str) -> str:
        # try:
        #     f = Fernet("t0uJb3hh87V02FMrwJtHSKGofdpTYn")
        #     password = f.decrypt(self.password_decode(password))
        # except:
        #     return ""
        # return password
        f = Fernet("t0uJb3hh87V02FMrwJtHSKGofdpTYn")
        password = f.decrypt(self.password_decode(password))
