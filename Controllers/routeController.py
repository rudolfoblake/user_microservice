from Controllers import inputController
ic = inputController.InputControl()
from DataBase import dataBase
db = dataBase.DataBase()
from Controllers import authController
ac = authController.AuthControl()


class RouteControl:
    def register_route(self, user_data: dict) -> tuple:
        verify_user_register_user_dataueriments = ic.verify_user_register_requirements(user_data)
        if verify_user_register_user_dataueriments[1] != 200: 
            return verify_user_register_user_dataueriments
        user_data['cpf'] = user_data['cpf'].replace(".", "").replace("-", "")
        get_email = db.get_user_by_email(user_data["email"])
        if get_email[1] == 200:
            if get_email[0]:
                return "Error: A user with that email already exists.", 400
        else:
            return get_email[0], get_email[1]
        if not ac.password_is_encoded(user_data['password']):
            encode_password = ac.password_encode(user_data['password'])
            if encode_password == "":
                return "Error: Failed to encode password!", 500
            user_data['password'] = encode_password
        user_data['password'] = str(user_data['password'])
        insert_user_in_database = db.create_user(user_data)
        return insert_user_in_database


    def get_user_by_id_route(self, id):
        return db.get_user_by_id(db.id_creation(id))
