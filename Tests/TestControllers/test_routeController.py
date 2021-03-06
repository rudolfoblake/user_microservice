from unittest import TestCase, mock

from bson import ObjectId

from Controllers import routeController
from Controllers.routeController import RouteControl
from DataBase.dataBase import DataBase

rc = routeController.RouteControl()

class TestRouteController(TestCase):
    @mock.patch("DataBase.dataBase.DataBase.create_user")
    @mock.patch("Controllers.inputController.InputControl.encrypt_register_data")
    @mock.patch("Controllers.authController.AuthControl.password_decode")
    @mock.patch("Controllers.authController.AuthControl.password_is_encoded")
    @mock.patch("DataBase.dataBase.DataBase.get_user_by_email")
    @mock.patch("Controllers.inputController.InputControl.verify_user_register_requirements")
    def test_register_route_works(self, mock_verify_user_register_requirements, mock_get_user_by_email, mock_password_is_encoded, mock_password_decode, mock_encrypt_register_data, mock_create_user):
        user_data = dict(
            first_name="Carlos", 
            last_name="Antonio", 
            email="email@email.com",
            password="pass",
            cpf="000.000.000-00",
            date_of_birth="00/00/0000"
        )
        mock_encrypt_register_data.return_value = user_data
        mock_verify_user_register_requirements.return_value = ("", 400)
        self.assertEqual(rc.register_route(user_data)[1], 400)

        mock_verify_user_register_requirements.return_value = ("", 200)
        mock_get_user_by_email.return_value = ([''], 400)
        self.assertEqual(rc.register_route(user_data)[1], 400)

        mock_get_user_by_email.return_value = ([''], 401)
        self.assertEqual(rc.register_route(user_data)[1], 400)

        mock_password_is_encoded.return_value = True
        mock_password_decode.return_value = ""
        mock_get_user_by_email.return_value = ([''], 404)
        self.assertEqual(rc.register_route(user_data)[1], 500)
        
        mock_password_is_encoded.return_value = True
        mock_password_decode.return_value = "test"
        mock_get_user_by_email.return_value = ([''], 404)
        mock_create_user.return_value = ("", 201)
        self.assertEqual(rc.register_route(user_data)[1], 201)

    @mock.patch("Controllers.inputController.InputControl.decrypt_address_data")
    @mock.patch("DataBase.dataBase.DataBase.id_creation")
    @mock.patch("DataBase.dataBase.DataBase.get_user_by_id")
    def test_get_user_by_id_route(self, mock_get_user_by_id, mock_id_creation, mock_decrypt_address_data):
        mock_id_creation.return_value = ObjectId("60a1444b370ea792caef5419")
        mock_get_user_by_id.return_value = ((dict()), 200)
        self.assertEqual(rc.get_user_by_id_route("60a1444b370ea792caef5419")[1], 200)
        mock_get_user_by_id.return_value = ((dict(address=[{
            "address_number": 77,
			"address_neighbourhood": "Bairro",
			"address_postal_code": "00000000",
			"address_city": "Florian??polis",
			"address_state": "SC"
        }])), 200)
        mock_decrypt_address_data.return_value = [{
            "address_number": 77,
			"address_neighbourhood": "Bairro",
			"address_postal_code": "00000000",
			"address_city": "Florian??polis",
			"address_state": "SC"
        }]

        self.assertEqual(rc.get_user_by_id_route("60a1444b370ea792caef5419")[1], 200)

    
    @mock.patch("DataBase.dataBase.DataBase.find_users_by_id")
    def test_get_users_by_id_route(self, mock_users_by_id_route):
        mock_users_by_id_route.side_effect = [({}, 200),  ({}, 400)]
        self.assertEqual(RouteControl().get_users_by_id_route({"_id":""}), ({}, 200))
        self.assertEqual(RouteControl().get_users_by_id_route({"_id":""}), ({}, 400))


    @mock.patch("Controllers.authController.AuthControl.decrypt")
    @mock.patch("Controllers.authController.AuthControl.is_encrypted")
    @mock.patch("DataBase.dataBase.DataBase.get_user_by_email")
    @mock.patch("Controllers.authController.AuthControl.password_decode")
    @mock.patch("Controllers.authController.AuthControl.password_is_encoded")
    @mock.patch("Controllers.inputController.InputControl.verify_user_login_requirements")
    def test_login_route_works(self, mock_verify_user_login_requirements, mock_password_is_encoded, mock_password_decode, mock_get_user_by_email, mock_is_encrypted, mock_decrypt):
        mock_is_encrypted.return_value = False
        user_data = dict(
            email="",
            password="testingpassword"
        )
        mock_verify_user_login_requirements.return_value = ("", 400)
        self.assertEqual(rc.login_route(user_data)[1], 400)
        mock_verify_user_login_requirements.return_value = ("", 200)
        mock_password_is_encoded.return_value = True
        mock_password_decode.return_value = ""
        self.assertEqual(rc.login_route(user_data)[1], 500)
        mock_password_decode.return_value = "x"
        mock_get_user_by_email.return_value = ([], 200)
        self.assertEqual(rc.login_route(user_data)[1], 400)
        mock_get_user_by_email.return_value = ([], 400)
        self.assertEqual(rc.login_route(user_data)[1], 400)
        mock_get_user_by_email.return_value = (dict(_id=""), 200)
        self.assertEqual(rc.login_route(user_data)[1], 500)
        mock_get_user_by_email.return_value = (dict(_id="wadwadasdfser", password="awdasdfw"), 200)
        mock_password_decode.side_effect = ["x", ""]
        self.assertEqual(rc.login_route(user_data)[1], 500)
        mock_password_decode.side_effect = ["x", "y"]
        mock_get_user_by_email.return_value = (dict(_id="wadwadasdfser", password="dawd"), 200)
        self.assertEqual(rc.login_route(user_data)[1], 401)
        mock_password_decode.side_effect = ["testingpassword", "X"]
        mock_is_encrypted.return_value = True
        mock_decrypt.return_value = "testingpassword"
        self.assertEqual(rc.login_route(user_data)[1], 200)

    @mock.patch("Controllers.authController.AuthControl.decrypt")
    @mock.patch("Controllers.mailController.MailControl.send_mail")
    @mock.patch("Controllers.tokenController.Token.generate_token")
    @mock.patch("DataBase.dataBase.DataBase.get_user_by_email")
    def test_recover_route_works(self, mock_get_user_by_email, mock_generate_token, mock_send_mail, mock_decrypt):
        token = {
                "token_id": "XjfWHiXtQltejTQpPXSp",
                "user_id": "UWfDaRdIdzhGaNeMTX9L",
                "expire": 14868846548.185464 #Validade de 15 minutos nos tokens
            }
        mock_decrypt.return_vaue = "UWfDaRdIdzhGaNeMTX9L"
        mock_get_user_by_email.return_value = ("", 404)
        self.assertEqual(rc.recover_route("myemail@email.com")[1], 404)

        mock_get_user_by_email.return_value = ({"_id":"UWfDaRdIdzhGaNeMTX9L"}, 200)
        mock_generate_token.return_value = None
        self.assertEqual(rc.recover_route("myemail@email.com")[1], 500)

        mock_get_user_by_email.return_value = ({"_id":"UWfDaRdIdzhGaNeMTX9L", "first_name": "Carlos"}, 200)
        mock_generate_token.return_value = token
        mock_send_mail.return_value = False
        self.assertEqual(rc.recover_route("myemail@email.com")[1], 400)

        mock_get_user_by_email.return_value = ({"_id":"UWfDaRdIdzhGaNeMTX9L", "first_name": "Carlos"}, 200)
        mock_generate_token.return_value = token
        mock_send_mail.return_value = True
        self.assertEqual(rc.recover_route("myemail@email.com")[1], 200)

    @mock.patch("Controllers.tokenController.Token.verify_token")
    def test_validate_recover_route_works(self, mock_verify_token):
        token_id = "yj39iB36iT9CRjqVBbmE"
        user_id = "Uh4QLMyg97WIvVCEPnE4"
        mock_verify_token.return_value = ""
        self.assertEqual(rc.validate_recover_route(token_id)[1], 404)

        mock_verify_token.return_value = user_id
        self.assertEqual(rc.validate_recover_route(token_id)[1], 200)
        self.assertEqual(rc.validate_recover_route(token_id)[0], user_id)

    @mock.patch("DataBase.dataBase.DataBase.update_user_by_id")
    @mock.patch("Controllers.inputController.InputControl.verify_address_requirements")
    def test_set_address_route_works(self, mock_verify_address, mock_update_user_by_id):
        mock_verify_address.return_value = ("", 400)
        address_data = dict(_id="gpwc6vvVtaGGxevXMfZV", address=[])
        self.assertEqual(rc.set_address_route(address_data, "60a9407d0fcea")[1], 400)
        mock_verify_address.return_value = ("", 200)
        mock_update_user_by_id.return_value = ("", 200)
        self.assertEqual(rc.set_address_route(address_data, "60a9407d0fcea")[1], 200)

    @mock.patch("DataBase.dataBase.DataBase.id_creation")
    @mock.patch("DataBase.dataBase.DataBase.update_user_by_id")
    @mock.patch("DataBase.dataBase.DataBase.get_user_by_id")
    @mock.patch("Controllers.inputController.InputControl.verify_change_password_requirements")
    def test_change_password_route_works(self, mock_verify_change_password_requirements, mock_get_user_by_id, mock_update_user_by_id, mock_id_creation):
        user_data = {
            "_id": "BTHuG6MsK4n8",
            "new_password": "Y0Umj8hRCRHS"
        }
        mock_verify_change_password_requirements.return_value = ("error test", 400)
        self.assertEqual(rc.change_password_route(user_data)[1], 400)
        mock_verify_change_password_requirements.return_value = ("error test", 200)
        mock_get_user_by_id.return_value = ("error test", 404)
        self.assertEqual(rc.change_password_route(user_data)[1], 404)
        mock_get_user_by_id.return_value = ("error test", 200)
        mock_update_user_by_id.return_value = ("success test", 200)
        mock_id_creation.return_value = "BTHuG6MsK4n8"
        self.assertEqual(rc.change_password_route(user_data)[1], 200)

