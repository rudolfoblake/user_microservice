from Controllers import inputController
ic = inputController.InputControl()
from DataBase import dataBase
db = dataBase.DataBase()
from Controllers import authController
ac = authController.AuthControl()
from Controllers import mailController
mc = mailController.MailControl()
from Controllers import tokenController
tc = tokenController.Token()
from config import CRYPT_KEY


class RouteControl:
    def register_route(self, user_data: dict) -> tuple:
        """Controller da rota de registro
        Conferir os dados enviados, verificar se o email já existe no banco de dados e registrar um novo usuário.

        Args:
            user_data (dict): Dicionário com as informações do usuário.

        Returns:
            tuple(content, statuscode): Retorna o id do usuário registrado e o statuscode, em caso de erro retorna a mensagem de erro.
        """
        verify_user_register_user_requirements = ic.verify_user_register_requirements(user_data)
        if verify_user_register_user_requirements[1] != 200: 
            return verify_user_register_user_requirements
        user_data['cpf'] = user_data['cpf'].replace(".", "").replace("-", "")
        get_email = db.get_user_by_email(user_data["email"])
        if not get_email[1] == 404:
            if get_email[1] == 400:
                return get_email
            else:
                return "Error: A user with that email already exists.", 400
        if ac.password_is_encoded(user_data['password']):
            decoded_password = ac.password_decode(user_data['password'])
            if decoded_password == "":
                return "Error: Failed to decode password!", 500
            user_data['password'] = decoded_password
        user_data = ic.encrypt_register_data(user_data)
        insert_user_in_database = db.create_user(user_data)
        return insert_user_in_database

    def login_route(self, user_data: dict) -> tuple:
        """Controller da rota de login
        Conferir se existe um usuário com o email enviado e verificar se a senha enviada é igual a senha do banco de dados.

        Args:
            user_data (dict): Dicionário com informações do usuário.

        Returns:
            tuple: Retorna o id do usuário conectado e o statuscode, em caso de erro retorna a mensagem de erro e o statuscode. 
        """
        verify_user_login_requirements = ic.verify_user_login_requirements(user_data)
        if verify_user_login_requirements[1] != 200:
            return verify_user_login_requirements
        if ac.password_is_encoded(user_data['password']):
            decode_password = ac.password_decode(user_data['password'])
            if decode_password == "":
                return "Error: Failed to decode password!", 500
            user_data['password'] = str(decode_password)
        get_user_by_email = db.get_user_by_email(user_data["email"])
        if get_user_by_email[1] == 200 or get_user_by_email[1] == 201:
            if not get_user_by_email[0]:
                return "Error: A user with that email does not exists.", 400
        else:
            return get_user_by_email
        try:
            get_user_by_email[0]['password']
        except:
            return "Error: Cannot get password from user on database to compare.", 500
        if ac.password_is_encoded(get_user_by_email[0]['password']):
            decode_database_password = ac.password_decode(get_user_by_email[0]['password'])
            if decode_database_password == "":
                return "Error: Failed to decode database password!", 500
            get_user_by_email[0]['password'] = str(decode_database_password)
        if ac.is_encrypted(get_user_by_email[0]['password'], CRYPT_KEY):
            get_user_by_email[0]['password'] = ac.decrypt(get_user_by_email[0]['password'], CRYPT_KEY)
        if get_user_by_email[0]['password'] != user_data['password']:
            return "Error: Invalid password!", 401
        return get_user_by_email[0]['_id'], 200

    def recover_route(self, email: str) -> tuple:
        """Controller da rota de recuperação de email
        Receber o email, verificar a sua existencia e gerar e enviar por email um token temporário para a recuperação da conta.

        Args:
            email (str): Email da conta do usuário a ser recuperada.

        Returns:
            tuple: tuple(content, statuscode): Retorna uma mensagem de sucesso e o statuscode, em caso de erro retorna a mensagem e o statuscode.
        """
        get_user_by_email = db.get_user_by_email(email)
        if get_user_by_email[1] != 200:
            return get_user_by_email
        token = tc.generate_token(get_user_by_email[0]['_id'])
        if token == None:
            return "Error: Cannot generate token.", 500
        if not mc.send_mail(email, "Recuperação de Conta Livro para Todxs", f"Olá {get_user_by_email[0]['first_name']}, clique no link a baixo para redefinir sua senha.\n\nhttp://localhost:5030/user/auth/token/{token['token_id']}\n\nLembrando que seu link é valido por 15 minutos!"):
            return "Error: Cannot send recover email.", 400
        return "Success: Token generated with success!", 200
    
    def validate_recover_route(self, token: str) -> tuple:
        """Controller da rota de verificação de token
        Receber o token, verificar a sua validade e retornar o id do usuário caso o token seja válido.

        Args:
            token (str): Token de recuperação de conta.

        Returns:
            tuple(content, statuscode): Retorna o ID do usuário e o statuscode, em caso de erro retorna a mensagem e o statuscode.
        """
        user_id = tc.verify_token(token)
        if user_id == "":
            return "Error: Invalid token!", 404
        return user_id, 200
    
    def set_address_route(self, address_data):
        """Controller da rota de endereço
        Conferir os dados recebidos e atualizar o endereço do usuário no banco de dados.

        Args:
            address_data (dict): Dicionário com informações do endereço.

        Returns:
            tuple: Retornar o ID do usuário que teve o endereço alterado com o código 200, retornando em caso de problema uma mensagem de erro e o statuscode.
        """
        verify_address = ic.verify_address_requirements(address_data)
        if verify_address[1] != 200:
            return verify_address
        return db.update_user_by_id(db.id_creation(address_data['_id']), dict(address=address_data['address']))

    def get_user_by_id_route(self, id):
        return db.get_user_by_id(db.id_creation(id))

    def get_users_by_id_route(self, list_id):
        return db.find_users_by_id(list_id["_id"])
        
       