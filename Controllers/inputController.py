import json

class InputControl:
     def json_to_dict(self, request):
          try:
               req = request.get_json()
          except:
               return 'Error: Cannot convert data into json!', 400
          return req, 200

     def verify_user_register_requirements(self, req: dict) -> tuple:
          try:
               req['email']
               req['password']
          except:
               return "Error: Requirements (email and password) not found at json", 400
          return "Success", 200
