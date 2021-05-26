from re import split
import uuid
import time

tokens = []

class Token:
    def save_token(self, token:dict):
        """Método para salvar o token
        Salvar o token em memória.

        Args:
            token (dict): Token do usuário.
        """
        tokens.append(token)

    def delete_token(self, token_index:int):
        """Método para apagar o token
        Apagar o token da memória.

        Args:
            token_index (int): Index do token a ser removido.
        """
        tokens.pop(token_index)

    def generate_token(self, user_id:str) -> dict:
        """Método para gerar um novo token
        Gerar um novo token com um id aleatório, o id do usuário e a validade.

        Args:
            user_id (str): ID do usuário a ser inserido dentro do token.

        Returns:
            dict: Retorna o token do usuário com token_id, user_id e expire.
        """
        token = {
                "token_id": str(uuid.uuid4()).split("-")[0],
                "user_id": user_id,
                "expire": time.time() + (15 * 60) #Validade de 15 minutos nos tokens
            }
        self.save_token(token)
        return token

    def verify_token(self, token_id:str) -> str:
        """Método para verificar a validade do token
        Verificar se o token existe e se é válido.

        Args:
            token_id (str): ID do token.

        Returns:
            str: Retorna o ID do usuário caso o token seja válido ou uma string vázia caso não seja.
        """
        user_id = ""
        for i in range(len(tokens)):
            if token_id == tokens[i]['token_id']:
                if tokens[i]['expire'] >= time.time():
                    selected_token = i
                    user_id = tokens[i]['user_id']
                else:
                    self.delete_token(i)
        if user_id != "":
            self.delete_token(selected_token)
        return user_id