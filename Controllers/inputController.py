import json
from validate_docbr import CPF
from email_validator import validate_email, EmailNotValidError
from Controllers import authController
ac = authController.AuthControl()
import datetime
import string
import re

class InputControl:
     def json_to_dict(self, request:json) -> tuple:
          """Converte json para dicionário
          Verificar a existência do recebimento de um json e transformar em dicionário para ser processado posteriormente.

          Args:
              request (json): Json recebido.

          Returns:
              tuple (content, statuscode): Retorna o dicionário com os itens do json e o código 200,
               em caso de erro retorna a mensagem de erro e o statuscode.
          """
          try:
               user_data = request.get_json()
          except:
               return 'Error: Cannot convert data into json!', 400
          return user_data, 200

     def verify_user_register_requirements(self, user_data: dict) -> tuple:
          """Verifica os requerimentos para registrar um usuário.
          Verificar a validade das informações recebidas no json.

          Args:
              user_data (dict): Dicionário com as informações para registro de usuário,
               informações básicas (first_name, last_name, cpf, email, date_of_birth, password)

          Returns:
              tuple: Retorna o statuscode e uma mensagem de erro, caso o statuscode não seja igual a 200 significa que a validação falhou!
          """
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

     def verify_address_requirements(self, address_data: dict) -> tuple:
          try:
               address_data['_id']
               if not type(address_data['address']) == list:
                    return "Error: address need be a list", 400
               for i in range(len(address_data['address'])):
                    if type(address_data['address'][i]['address_number']) != int:
                         return "Error: address number need be a int", 400
                    if type(address_data['address'][i]['address_neighbourhood']) != str:
                         return "Error: address neighbourhood needs be a string", 400
                    if type(address_data['address'][i]['address_postal_code']) != str:
                         return "Error: address postal code needs be a int", 400
                    if type(address_data['address'][i]['address_city']) != str:
                         return "Error: address city needs be a string", 400
                    if type(address_data['address'][i]['address_state']) != str:
                         return "Error: address state needs be a string", 400
          except:
               return "Error: Requeriments (_id, address[address_number, address_neighbourhood, address_postal_code, address_city, address_state]) not found on json", 400
          return "Success", 200

     def verify_user_login_requirements(self, user_data: dict) -> tuple:
          """Verifica os requerimentos para login do usuário.
          Verificar a validade das informações recebidas no json.

          Args:
              user_data (dict): Dicionário com as informações para login do usuário, informações básicas (email, password)

          Returns:
              tuple: Retorna o statuscode e uma mensagem de erro, caso o statuscode não seja igual a 200 significa que a validação falhou!
          """
          try:
               user_data['email']
               user_data['password']
          except:
               return "Error: User information (email, password) not found in json.", 400
          return "Success", 200

     def verify_first_name(self, first_name: str) -> bool:
          """Verifica o primeiro nome do usuário.
          Verificar o primeiro nome do usuário, validando seu tamanho e verificando os caracteres presentes.

          Args:
              first_name (str): Primeiro nome do usuário.

          Returns:
              bool: Retorna true ou false, caso retorne true significa que o nome é válido.
          """
          if len(first_name) < 2 or len(first_name) > 30:
               return False
          res = re.findall(r'([A-Za-zÀ-ÿ]+)', first_name, re.UNICODE)
          if not len(res) or not res[0] == first_name:
               return False
          return True

     def verify_last_name(self, last_name: str) -> bool:
          """Verifica o sobrenome do usuário.
          Verificar o sobrenome do usuário, validando seu tamanho e verificando os caracteres presentes.

          Args:
              last_name (str): Sobrenome do usuário.

          Returns:
              bool: Retorna true ou false, caso retorne true significa que o sobrenome é válido.
          """
          if len(last_name) < 2 or len(last_name) > 60:
               return False
          res = re.findall(r'([A-Za-zÀ-ÿ]+)', last_name, re.UNICODE)
          if not len(res) or not res[0] == last_name:
               return False
          return True

     def verify_password(self, password: str):
          """Verifica a senha do usuário.
          Verificar a senha do usuário, a fim de garantir que não sejam aceitas senhas com caracteres inválidos.

          Args:
              password (str): Senha do usuário.

          Returns:
              [type]: Retorna true ou false, caso retorne true significa que a senha é válida.
          """
          if len(password) > 50 or len(password) < 6:
               return False
          if not all(char in string.punctuation or char == " " or char.isalpha() or char.isdigit() for char in password):  
               return False
          return True

     def validate_cpf(self, cpf: str) -> bool:
          """Verifica o CPF do usuário.
          Verificar o cpf do usuário, a fim de garantir que ele seja um CPF real.

          Args:
               cpf (str): CPF do usuário.

          Returns:
               bool: Retorna true ou false, caso retorne true significa que o CPF é válido.
          """
          if CPF().validate(cpf):
               return True
          else:
               return False

     def validate_email(self, email: str) -> bool:
          """Verifica o email do usuário.
          Verificar o email do usuário, a fim de garantir que o mesmo seja um email existente.

          Args:
              email (str): Email do usuário.

          Returns:
              bool: Retorna true ou false, caso retorne true significa que o email é válido.
          """
          try:
               valid = validate_email(email, allow_smtputf8=True, check_deliverability=True)
          except EmailNotValidError:
               return False
          return True

     def validate_date_of_birth(self, birth: str) -> bool:
          """Verifica a data de nascimento do usuário.
          Verificar a data de nascimento do usuário, a fim de garantir que seja uma data de nascimento real no formato correto.

          Args:
              birth (str): Data de nascimento do usuário.

          Returns:
              bool: Retorna true ou false, caso retorne true significa que uma data de nascimento válida.
          """
          try:
               datetime.datetime.strptime(birth, "%m/%d/%Y")
          except:
               return False
          return True

     def encrypt_register_data(self, user_data:dict) -> dict:
          if not ac.is_encrypted(user_data['first_name']):
               user_data['first_name'] = ac.encrypt(user_data['first_name'], "K22eIoXBwOnMuJL6nRo0GOIZLGNgGa_diB_FJvUa3AY=")
          if not ac.is_encrypted(user_data['last_name']):
               user_data['last_name'] = ac.encrypt(user_data['last_name'], "K22eIoXBwOnMuJL6nRo0GOIZLGNgGa_diB_FJvUa3AY=")
          if not ac.is_encrypted(user_data['cpf']):
               user_data['cpf'] = ac.encrypt(user_data['cpf'], "K22eIoXBwOnMuJL6nRo0GOIZLGNgGa_diB_FJvUa3AY=")
          if not ac.is_encrypted(user_data['password']):
               user_data['password'] = ac.encrypt(user_data['password'], "K22eIoXBwOnMuJL6nRo0GOIZLGNgGa_diB_FJvUa3AY=")
          try:
               if not ac.is_encrypted(user_data['phone_number']):
                    user_data['phone_number'] = ac.encrypt(user_data['phone_number'], "K22eIoXBwOnMuJL6nRo0GOIZLGNgGa_diB_FJvUa3AY=")
          except:
               pass
          return user_data