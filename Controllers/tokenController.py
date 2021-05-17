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
        is_valid = False
        for i in range(len(tokens)):
            if token_id['token_id'] == tokens[i]['token_id']:
                print("Achou!")
                if tokens[i]['time'] >= time.time():
                    is_valid = True
        return is_valid