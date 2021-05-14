from Controllers import inputController
ic = inputController.InputControl()
from DataBase import dataBase
db = dataBase.DataBase()
from Controllers import authController
ac = authController.AuthControl()


class RouteControl:
    def register_route(self, user_data: dict) -> tuple:
        verify_user_register_user_requirements = ic.verify_user_register_requirements(user_data)
        if verify_user_register_user_requirements[1] != 200: 
            return verify_user_register_user_requirements
        user_data['cpf'] = user_data['cpf'].replace(".", "").replace("-", "")
        get_email = db.get_user_by_email(user_data["email"])
        if get_email[1] == 200:
            if get_email[0]:
                return "Error: A user with that email already exists.", 400
        else:
            return get_email
        if not ac.password_is_encoded(user_data['password']):
            encode_password = ac.password_encode(user_data['password'])
            if encode_password == "":
                return "Error: Failed to encode password!", 500
            user_data['password'] = str(encode_password)
        insert_user_in_database = db.create_user(user_data)
        return insert_user_in_database

    def login_route(self, user_data: dict) -> tuple:
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


    def get_user_by_id_route(self, id):
        return db.get_user_by_id(db.id_creation(id))
