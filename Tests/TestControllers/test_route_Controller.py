from unittest import TestCase, mock
from Controllers import routeController
rc = routeController.RouteControl()

class TestRouteController(TestCase):
    @mock.patch("Controllers.authController.AuthControl.password_encode")
    @mock.patch("Controllers.authController.AuthControl.password_is_encoded")
    @mock.patch("DataBase.dataBase.DataBase.get_user_by_email")
    @mock.patch("Controllers.inputController.InputControl.verify_user_register_requirements")
    def test_register_route_works(self, mock_verify_user_register_requirements, mock_get_user_by_email, mock_password_is_encoded, mock_password_encode):
        user_data = dict(
            first_name="Carlos", 
            last_name="Antonio", 
            email="email@email.com",
            password="pass",
            cpf="000.000.000-00",
            date_of_birth="00/00/0000"
        )
        mock_verify_user_register_requirements.return_value = ("", 400)
        self.assertEqual(rc.register_route(user_data)[1], 400)
        mock_verify_user_register_requirements.return_value = ("", 200)
        mock_get_user_by_email.return_value = ([''], 200)
        self.assertEqual(rc.register_route(user_data)[1], 400)
        mock_get_user_by_email.return_value = ([''], 400)
        self.assertEqual(rc.register_route(user_data)[1], 400)
        mock_get_user_by_email.return_value = ([], 200)
        mock_password_is_encoded.return_value = False
        mock_password_encode.return_value = ""
        self.assertEqual(rc.register_route(user_data)[1], 500)
        mock_password_encode.return_value = "test"
        self.assertEqual(rc.register_route(user_data)[1], 200)

    @mock.patch("DataBase.dataBase.DataBase.get_user_by_email")
    @mock.patch("Controllers.authController.AuthControl.password_decode")
    @mock.patch("Controllers.authController.AuthControl.password_is_encoded")
    @mock.patch("Controllers.inputController.InputControl.verify_user_login_requirements")
    def test_login_route_works(self, mock_verify_user_login_requirements, mock_password_is_encoded, mock_password_decode, mock_get_user_by_email):
        user_data = dict(
            email="",
            password=""
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
        mock_password_decode.side_effect = ["x", "x"]
        self.assertEqual(rc.login_route(user_data)[1], 200)

    @mock.patch("DataBase.dataBase.DataBase.update_user_by_id")
    @mock.patch("Controllers.inputController.InputControl.verify_address_requirements")
    def test_set_address_route_works(self, mock_verify_address, mock_update_user_by_id):
        mock_verify_address.return_value = ("", 400)
        address_data = dict(_id="gpwc6vvVtaGGxevXMfZV", address=[])
        self.assertEqual(rc.set_address_route(address_data)[1], 400)
        mock_verify_address.return_value = ("", 200)
        mock_update_user_by_id.return_value = ("", 200)
        self.assertEqual(rc.set_address_route(address_data)[1], 200)
