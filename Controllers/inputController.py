import json

class InputControl:
     def json_to_dict(self, request:json) -> tuple:
          try:
               req = request.get_json()
          except:
               return 'Error: Cannot convert data into json!', 400
          return req, 200

     def verify_user_register_requirements(self, req: dict) -> tuple:
          try:
               req['first_name']
               req['last_name']
               req['email']
               req['password']
               req['cpf']
               req['date_of_birth']
               #req['address']
          except:
               return "Error: Requirements (first_name, last_name, email, password, cpf, date_of_birth) not found at json", 400
          return "Success", 200
