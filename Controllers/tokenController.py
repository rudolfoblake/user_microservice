import uuid
import time
import datetime

tokens = []

class Token:
    def save_token(self, token:dict):
        tokens.append(token)

    def generate_token(self, id:str) -> dict:
        token = {
                "token_id": uuid.uuid4().hex,
                "user_id": id,
                "time": time.time() + 15 * 60
            }
        self.save_token(token)
        return token

    def verify_token(self, token_id:str):
        for i in range(len(token)):
            if token_id == token[i][id]:
                if toke[i][time] <= time.time():
                    return True
        return False