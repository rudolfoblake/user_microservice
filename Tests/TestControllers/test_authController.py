from unittest import TestCase, mock
from Controllers import authController
ac = authController.AuthControl()

class TestAuthController(TestCase):
    def test_password_encode_works(self):
        self.assertEqual(ac.password_encode("testepassword"), "dGVzdGVwYXNzd29yZA==")
        self.assertEqual(ac.password_encode([]), "")
        self.assertEqual(ac.password_encode({}), "")

    def test_password_is_encoded_works(self):
        self.assertFalse(ac.password_is_encoded("testpassword"))
        self.assertTrue(ac.password_is_encoded("dGVzdGVwYXNzd29yZA=="))

    def test_password_decode_works(self):
        self.assertEqual(ac.password_decode("dGVzdGVwYXNzd29yZA=="), "testepassword")
        self.assertEqual(ac.password_decode("test"), "")

