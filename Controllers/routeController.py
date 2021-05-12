import base64
from Controllers import inputController
ic = inputController.InputControl()
from DataBase import dataBase
db = dataBase()


class RouteControl:
    def register_route(self, req:dict) -> tuple:
        verify_user_register_requeriments = ic.verify_user_register_requirements(req)
        if verify_user_register_requeriments[1] != 200: return verify_user_register_requeriments
        get_email = db.get_user_by_email(req["email"])
        if get_email[1] == 200:
            if len(get_email[0]) > 0:
                return "Error: A user with that email already exists.", 400
        else:
            return get_email[0], get_email[1]

    def get_user_by_id_route(self, id):
        return db.get_user_by_id(db.id_creation(id))