import json
from validate_docbr import CPF
from email_validator import validate_email, EmailNotValidError
import datetime
import string

class InputControl:
     def json_to_dict(self, request:json) -> tuple:
          try:
               user_data = request.get_json()
          except:
               return 'Error: Cannot convert data into json!', 400
          return user_data, 200

     def verify_user_register_requirements(self, user_data: dict) -> tuple:
          try:
               user_data['first_name']
               user_data['last_name']
               user_data['email']
               user_data['password']
               user_data['cpf']
               user_data['date_of_birth']
               #user_data['address']
          except:
               return "Error: Requirements (first_name, last_name, email, password, cpf, date_of_birth) not found at json", 400
          if not self.verify_first_name(user_data['first_name']): 
               return "Error: Invalid first name.", 400
          if not self.verify_last_name(user_data['last_name']):
               return "Error: Invalid last name.", 400
          if not self.validate_cpf(user_data['cpf']):
               return "Error: Invalid CPF.", 400
          if not self.validate_email(user_data['email']):
               return "Error: Invalid Email.", 400
          if not self.validate_date_of_birth(user_data['date_of_birth']):
               return "Error: Invalid birth date.", 400
          return "Success", 200

     def verify_first_name(self, first_name: str) -> bool:
          if " " in first_name or len(first_name) < 3:
               return False
          for i in first_name:
            if not i in string.ascii_letters and not i == "é" and not i == "è" and not i == "ã" and not i == "á" and not i == "à":
                return False
          return True

     def verify_last_name(self, last_name: str) -> bool:
          if len(last_name) < 3:
               return False
          for i in last_name:
            if not i in string.ascii_letters and not i == "é" and not i == "è" and not i == "ã" and not i == "á" and not i == "à":
                return False
          return True

     def validate_cpf(self, cpf: str) -> bool:
        if CPF().validate(cpf):
            return True
        else:
            return False

     def validate_email(self, email: str) -> bool:
        try:
            valid = validate_email(email, allow_smtputf8=True, check_deliverability=True)
            email = valid.email
        except EmailNotValidError:
            return False
        return True

     def validate_date_of_birth(self, birth: str) -> bool:
          splited_birth = birth.split("/")
          if not len(splited_birth) == 3:
               return False
          for i in range(len(splited_birth)):
               try:
                    splited_birth[i] = int(splited_birth[i])
               except:
                    return False
               if i == 0:
                    if splited_birth[i] <= 0 or splited_birth[i] > 12:
                         return False
               elif i == 1:
                    if splited_birth[i] <= 0 or splited_birth[i] > 31:
                         return False
               elif i == 2:
                    if splited_birth[i] < 1900 or splited_birth[i] > int(datetime.datetime.now().year):
                         return False
          return True
