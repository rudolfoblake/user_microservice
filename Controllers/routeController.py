from Controllers import inputController
ic = inputController.InputControl()
from DataBase import dataBase
db = dataBase.DataBase()
from Controllers import authController
ac = authController.AuthControl()


class RouteControl:
    def register_route(self, req: dict) -> tuple:
        verify_user_register_requeriments = ic.verify_user_register_requirements(req)
        if verify_user_register_requeriments[1] != 200: 
            return verify_user_register_requeriments
        get_email = db.get_user_by_email(req["email"])
        if get_email[1] == 200:
            if get_email[0]:
                return "Error: A user with that email already exists.", 400
        else:
            return get_email[0], get_email[1]
        if not ac.password_is_encoded(req['password']):
            encode_password = ac.password_encode(req['password'])
            if encode_password == "":
                return "Error: Failed to encode password!", 500
            req['password'] = encode_password
        req['password'] = str(req['password'])
        insert_user_in_database = db.create_user(req)
        if insert_user_in_database[1] != 200:
            return insert_user_in_database
        return insert_user_in_database[0], 200


    def get_user_by_id_route(self, id):
        return db.get_user_by_id(db.id_creation(id))
