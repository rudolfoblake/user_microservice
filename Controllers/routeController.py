import base64
from Controllers import inputController
ic = inputController.InputControl()
base64

class RouteControl:
    def register_route(self, req:dict) -> tuple:
        verify_user_register_requeriments = ic.verify_user_register_requirements(req)
        if verify_user_register_requeriments[1] != 200: return verify_user_register_requeriments
        

        return req, 200
