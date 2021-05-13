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

    @mock.patch("Controllers.inputController.InputControl.validate_date_of_birth")
    @mock.patch("Controllers.inputController.InputControl.validate_email")
    @mock.patch("Controllers.inputController.InputControl.validate_cpf")
    @mock.patch("Controllers.inputController.InputControl.verify_last_name")
    @mock.patch("Controllers.inputController.InputControl.verify_first_name")
    def test_verify_user_register_requirements_works(self, mock_verify_first_name, mock_verify_last_name, mock_validate_cpf, mock_validate_email, mock_validate_date_of_birth):
        self.assertEqual(ic.verify_user_register_requirements(dict())[1], 400)
        mock_verify_first_name.return_value = True
        mock_verify_last_name.return_value = True
        mock_validate_cpf.return_value = True
        mock_validate_email.return_value = True
        mock_validate_date_of_birth.return_value = True
        req_values = dict(
            first_name="Carlos", 
            last_name="Antonio", 
            email="email@email.com",
            password="pass",
            cpf="000.000.000-00",
            date_of_birth="00/00/0000"
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

    def test_verify_first_name_works(self):
        self.assertFalse(ic.verify_first_name(" "))
        self.assertFalse(ic.verify_first_name("1111"))
        self.assertTrue(ic.verify_first_name("Carlos"))

    def test_verify_last_name_works(self):
        self.assertFalse(ic.verify_last_name(""))
        self.assertFalse(ic.verify_last_name("1234"))
        self.assertTrue(ic.verify_last_name("Antonio"))

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
        self.assertTrue(ic.validate_date_of_birth("12/31/2010"))