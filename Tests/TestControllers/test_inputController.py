import json
from unittest import TestCase, mock
from validate_docbr import CPF
from Controllers import inputController
ic = inputController.InputControl()

class TestInputController(TestCase):

    def test_json_to_dict_works(self):
        self.assertEqual(ic.json_to_dict("")[1], 400)
        mock_request = mock.Mock()
        mock_request.get_json.return_value = {"A":"B"}
        self.assertEqual(ic.json_to_dict(mock_request)[1], 200)

    @mock.patch("Controllers.inputController.InputControl.verify_password")
    @mock.patch("Controllers.inputController.InputControl.validate_date_of_birth")
    @mock.patch("Controllers.inputController.InputControl.validate_email")
    @mock.patch("Controllers.inputController.InputControl.validate_cpf")
    @mock.patch("Controllers.inputController.InputControl.verify_last_name")
    @mock.patch("Controllers.inputController.InputControl.verify_first_name")
    def test_verify_user_register_requirements_works(self, mock_verify_first_name, mock_verify_last_name, mock_validate_cpf, mock_validate_email, mock_validate_date_of_birth, mock_verify_password):
        self.assertEqual(ic.verify_user_register_requirements(dict())[1], 400)
        mock_verify_first_name.return_value = True
        mock_verify_last_name.return_value = True
        mock_validate_cpf.return_value = True
        mock_validate_email.return_value = True
        mock_validate_date_of_birth.return_value = True
        mock_verify_password.return_value = True
        req_values = dict(
            first_name="", 
            last_name="", 
            email="",
            password="",
            cpf="",
            date_of_birth=""
        )
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 200)
        mock_verify_first_name.return_value = False
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 400)
        mock_verify_first_name.return_value = True
        mock_verify_last_name.return_value = False
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 400)
        mock_verify_last_name.return_value = True
        mock_validate_cpf.return_value = False
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 400)
        mock_validate_cpf.return_value = True
        mock_validate_email.return_value = False
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 400)
        mock_validate_email.return_value = True
        mock_validate_date_of_birth.return_value = False
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 400)
        mock_validate_date_of_birth.return_value = True
        mock_verify_password.return_value = False
        self.assertEqual(ic.verify_user_register_requirements(req_values)[1], 400)

    def test_verify_address_requirements_works(self):
        address_data = dict()
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=""
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": ""
                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": 123,
                    "address_neighbourhood": 1
                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": 123,
                    "address_neighbourhood": "",
                    "address_postal_code": 0
                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": 123,
                    "address_neighbourhood": "",
                    "address_postal_code": "",
                    "address_city": 0
                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": 123,
                    "address_neighbourhood": "",
                    "address_postal_code": "",
                    "address_city": "",
                    "address_state": 0

                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 400)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": 123,
                    "address_neighbourhood": "",
                    "address_postal_code": "",
                    "address_city": "",
                    "address_state": ""

                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 200)
        address_data = dict(
            _id="3AWUsCCwog9cj5NBim8j",
            address=[
                {
                    "address_number": 123,
                    "address_neighbourhood": "",
                    "address_postal_code": "",
                    "address_city": "",
                    "address_state": ""

                },
                {
                    "address_number": 123,
                    "address_neighbourhood": "",
                    "address_postal_code": "",
                    "address_city": "",
                    "address_state": ""

                }
            ]
        )
        self.assertEqual(ic.verify_address_requirements(address_data)[1], 200)

    def test_verify_first_name_works(self):
        self.assertFalse(ic.verify_first_name(" "))
        self.assertFalse(ic.verify_first_name("a"))
        self.assertFalse(ic.verify_first_name("1111"))
        self.assertTrue(ic.verify_first_name("Carlos"))

    def test_verify_last_name_works(self):
        self.assertFalse(ic.verify_last_name(""))
        self.assertFalse(ic.verify_last_name("a"))
        self.assertFalse(ic.verify_last_name("1234"))
        self.assertTrue(ic.verify_last_name("Antonio"))

    def test_verify_password_works(self):
        self.assertFalse(ic.verify_password(""))
        self.assertFalse(ic.verify_password("☺☺☺☺☺☺"))
        self.assertTrue(ic.verify_password("123456"))
        self.assertTrue(ic.verify_password("ABCDEFG"))
        self.assertTrue(ic.verify_password("!@#$%&"))

    def test_verify_change_password_requirements_works(self):
        user_data = {"new_password": "123456"}
        self.assertEqual(ic.verify_change_password_requirements(user_data)[1], 400)
        user_data = {"_id": "iwkJ55AxTiJx", "new_password": "123"}
        self.assertEqual(ic.verify_change_password_requirements(user_data)[1], 400)
        user_data = {"_id": "iwkJ55AxTiJx", "new_password": "123456"}
        self.assertEqual(ic.verify_change_password_requirements(user_data)[1], 200)

    def test_validate_cpf_works(self):
        self.assertTrue(ic.validate_cpf(CPF().generate()))
        self.assertTrue(ic.validate_cpf(CPF().generate(True)))
        self.assertFalse(ic.validate_cpf("000.000.000-00"))

    def test_validate_email_works(self):
        self.assertFalse(ic.validate_email(""))
        self.assertTrue(ic.validate_email("email@email.com"))
        self.assertTrue(ic.validate_email("email@email.com.br"))

    def test_validate_date_of_birth_works(self):
        self.assertFalse(ic.validate_date_of_birth("00/00"))
        self.assertFalse(ic.validate_date_of_birth("aa/aa/aaaa"))
        self.assertFalse(ic.validate_date_of_birth("13/00/0000"))
        self.assertFalse(ic.validate_date_of_birth("12/32/0000"))
        self.assertFalse(ic.validate_date_of_birth("12/31/0000"))
        self.assertTrue(ic.validate_date_of_birth("12/20/2010"))

    def test_verify_user_login_requirements_works(self):
        user_data = dict()
        self.assertEqual(ic.verify_user_login_requirements(user_data)[1], 400)
        user_data = dict(email="", password="")
        self.assertEqual(ic.verify_user_login_requirements(user_data)[1], 200)

    @mock.patch("Controllers.authController.AuthControl.encrypt")
    @mock.patch("Controllers.authController.AuthControl.is_encrypted")
    def test_encrypt_register_data_works(self, mock_is_encrypted, mock_encrypt):
        user_data = dict(
            first_name="Carlos",
            last_name="Jose",
            cpf="0000000000",
            password="123456",
            phone_number="123456789"
        )
        encripted_user_data = dict(
            first_name=bytes("Carlos".encode()),
            last_name=bytes("Jose".encode()),
            cpf=bytes("0000000000".encode()),
            password=bytes("123456".encode()),
            phone_number=bytes("123456789".encode())
        )

        mock_is_encrypted.return_value = False
        mock_encrypt.side_effect = [
            encripted_user_data['first_name'],
            encripted_user_data['last_name'],
            encripted_user_data['cpf'],
            encripted_user_data['password'],
            encripted_user_data['phone_number']
        ]
        self.assertEqual(ic.encrypt_register_data(user_data), encripted_user_data)

        user_data = dict(
            first_name="Carlos",
            last_name="Jose",
            cpf="0000000000",
            password="123456"
        )
        encripted_user_data = dict(
            first_name=bytes("Carlos".encode()),
            last_name=bytes("Jose".encode()),
            cpf=bytes("0000000000".encode()),
            password=bytes("123456".encode())
        )
        mock_encrypt.side_effect = [
            encripted_user_data['first_name'],
            encripted_user_data['last_name'],
            encripted_user_data['cpf'],
            encripted_user_data['password']
        ]
        self.assertEqual(ic.encrypt_register_data(user_data), encripted_user_data)
