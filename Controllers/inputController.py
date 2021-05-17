import json
from validate_docbr import CPF
from email_validator import validate_email, EmailNotValidError
import datetime
import string
import re

class InputControl:
     def json_to_dict(self, request:json) -> tuple:
          try:
               user_data = request.get_json()
          except:
               return 'Error: Cannot convert data into json!', 400
          return user_data, 200

     def verify_user_register_requirements(self, user_data: dict) -> tuple:
          try:
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
               if not self.verify_password(user_data['password']):
                    return "Error: Invalid password.", 400
          except:
               return "Error: Requirements (first_name, last_name, email, password, cpf, date_of_birth) not found at json", 400
          return "Success", 200

     def verify_user_login_requirements(self, user_data: dict) -> tuple:
          try:
               user_data['email']
               user_data['password']
          except:
               return "Error: User information (email, password) not found in json.", 400
          return "Success", 200

     def verify_first_name(self, first_name: str) -> bool:
          if len(first_name) < 2 or len(first_name) > 30:
               return False
          res = re.findall(r'([A-Za-zÀ-ÿ]+)', first_name, re.UNICODE)
          if not len(res) or not res[0] == first_name:
               return False
          return True

     def verify_last_name(self, last_name: str) -> bool:
          if len(last_name) < 2 or len(last_name) > 60:
               return False
          res = re.findall(r'([A-Za-zÀ-ÿ]+)', last_name, re.UNICODE)
          if not len(res) or not res[0] == last_name:
               return False
          return True

     def verify_password(self, password: str):
          if len(password) > 50 or len(password) < 6:
               return False
          if not all(char in string.punctuation or char == " " or char.isalpha() or char.isdigit() for char in password):  
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
        except EmailNotValidError:
            return False
        return True

     def validate_date_of_birth(self, birth: str) -> bool:
          try:
               datetime.datetime.strptime(birth, "%m/%d/%Y")
          except:
               return False
          return True
