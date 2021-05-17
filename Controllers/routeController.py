from Controllers import inputController
ic = inputController.InputControl()
from DataBase import dataBase
db = dataBase.DataBase()
from Controllers import authController
ac = authController.AuthControl()


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
        if not ac.password_is_encoded(user_data['password']):
            encode_password = ac.password_encode(user_data['password'])
            if encode_password == "":
                return "Error: Failed to encode password!", 500
            user_data['password'] = str(encode_password)
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
        if get_user_by_email[1] == 200:
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
        if get_user_by_email[0]['password'] != user_data['password']:
            return "Error: Invalid password!", 401
        return get_user_by_email[0]['_id'], 200

    def recover_route(self, user_data):
        try:
            email = user_data['email']
        except:
            return "Error: Cannot found email into json", 400

        get_user_by_email = db.get_user_by_email(email)
        if get_user_by_email[1] != 200:
            return get_user_by_email
        
    
    def get_user_by_id_route(self, id):
        return db.get_user_by_id(db.id_creation(id))
